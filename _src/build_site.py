import os
import shutil
import json
import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timezone
from urllib.parse import urljoin
import re

SITE_NAME = "Extended Car Warranty Hub"
SITE_URL = "https://extended-car-warranty-fleet.bongshai.com"
AUTHOR_NAME = "Fleet Protection Expert"

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def build_site():
    print("Building site...")
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CONTENT_DIR = os.path.join(BASE_DIR, 'content')
    TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
    ASSETS_DIR = os.path.join(BASE_DIR, 'src_assets')
    
    # Target is the parent directory of _src
    PUBLIC_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
    
    # Initialize public dir, preserving _src, .git, .cpanel.yml
    protected_files = ['.git', '_src', '.cpanel.yml', '.gitignore', 'README.md']
    
    for filename in os.listdir(PUBLIC_DIR):
        if filename in protected_files:
            continue
        filepath = os.path.join(PUBLIC_DIR, filename)
        if os.path.isfile(filepath) or os.path.islink(filepath):
            os.unlink(filepath)
        elif os.path.isdir(filepath):
            import stat
            def remove_readonly(func, path, _):
                os.chmod(path, stat.S_IWRITE)
                func(path)
            shutil.rmtree(filepath, onerror=remove_readonly)

    # Copy assets directly to root or assets folder
    if os.path.exists(ASSETS_DIR):
        shutil.copytree(ASSETS_DIR, os.path.join(PUBLIC_DIR, 'assets'), dirs_exist_ok=True)
        # Move PWA files to root
        for pwa_file in ['sw.js', 'manifest.json']:
            src = os.path.join(PUBLIC_DIR, 'assets', pwa_file)
            if os.path.exists(src):
                shutil.move(src, os.path.join(PUBLIC_DIR, pwa_file))
    
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'])
    
    articles = []
    pages = []
    search_index = []
    
    def process_md_file(file_path, template_name, url_prefix=""):
        with open(file_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
            
        slug = post.metadata.get('slug', os.path.splitext(os.path.basename(file_path))[0])
        url_path = f"{url_prefix}{slug}/" if url_prefix else f"/{slug}/"
        if slug == "index":
            url_path = "/"
            
        html_content = md.convert(post.content)
        
        page_data = {
            'title': post.metadata.get('title', 'Untitled'),
            'description': post.metadata.get('description', ''),
            'keyword': post.metadata.get('keyword', ''),
            'author': post.metadata.get('author', AUTHOR_NAME),
            'date': post.metadata.get('date', datetime.now(timezone.utc).strftime('%Y-%m-%d')),
            'content': html_content,
            'url': url_path,
            'slug': slug,
            'is_article': url_prefix == "/articles/",
            'last_updated': post.metadata.get('last_updated', post.metadata.get('date', datetime.now(timezone.utc).strftime('%Y-%m-%d'))),
            'raw_content': post.content
        }
        
        search_index.append({
            'title': page_data['title'],
            'url': page_data['url'],
            'content': post.content[:200] + '...'
        })
        
        return page_data

    # Parse articles
    articles_dir = os.path.join(CONTENT_DIR, 'articles')
    if os.path.exists(articles_dir):
        for filename in os.listdir(articles_dir):
            if filename.endswith('.md'):
                file_path = os.path.join(articles_dir, filename)
                data = process_md_file(file_path, 'article.html', url_prefix="/articles/")
                articles.append(data)
                
    articles.sort(key=lambda x: x['date'], reverse=True)
    
    # Parse individual pages
    pages_dir = os.path.join(CONTENT_DIR, 'pages')
    if os.path.exists(pages_dir):
        for filename in os.listdir(pages_dir):
            if filename.endswith('.md'):
                file_path = os.path.join(pages_dir, filename)
                data = process_md_file(file_path, 'article.html', url_prefix="/")
                pages.append(data)
                
    # Parse legal pages
    legal_dir = os.path.join(CONTENT_DIR, 'legal')
    if os.path.exists(legal_dir):
        for filename in os.listdir(legal_dir):
            if filename.endswith('.md'):
                file_path = os.path.join(legal_dir, filename)
                data = process_md_file(file_path, 'article.html', url_prefix="/legal/")
                pages.append(data)
                
    # Parse standalone pages
    for filename in ['about.md', 'contact.md', 'index.md', '404.md']:
        file_path = os.path.join(CONTENT_DIR, filename)
        if os.path.exists(file_path):
            data = process_md_file(file_path, 'article.html', url_prefix="/")
            if data['slug'] == 'index':
                data['url'] = '/'
            pages.append(data)
            
    all_content = articles + pages
    for item in all_content:
        template_name = 'article.html'
        if item['slug'] == 'index':
            template_name = 'index.html'
        elif item['slug'] == '404':
            template_name = '404.html'
            
        template = env.get_template(template_name)
        related_articles = [a for a in articles if a['slug'] != item['slug']][:3]
        
        # Build Schema (Article & FAQ)
        schemas = []
        if item['is_article']:
            schemas.append({
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": item['title'],
                "author": {"@type": "Person", "name": item['author']},
                "datePublished": item['date'],
                "dateModified": item['last_updated']
            })
            # Simple FAQ extraction
            faq_pattern = r"\*\*Q: (.*?)\*\*\s*A: (.*?)(?=\*\*Q:|$)"
            faqs = re.findall(faq_pattern, item['raw_content'], re.DOTALL)
            if faqs:
                faq_schema = {
                    "@context": "https://schema.org",
                    "@type": "FAQPage",
                    "mainEntity": []
                }
                for q, a in faqs:
                    faq_schema["mainEntity"].append({
                        "@type": "Question",
                        "name": q.strip(),
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": a.strip()
                        }
                    })
                schemas.append(faq_schema)
                
        output_html = template.render(
            page=item,
            site_name=SITE_NAME,
            site_url=SITE_URL,
            articles=articles,
            related_articles=related_articles,
            current_year=datetime.now(timezone.utc).year,
            schemas=schemas
        )
        
        if item['url'] == '/':
            out_file = os.path.join(PUBLIC_DIR, 'index.html')
        elif item['slug'] == '404':
            out_file = os.path.join(PUBLIC_DIR, '404.html')
        else:
            out_dir = os.path.join(PUBLIC_DIR, item['url'].strip('/'))
            ensure_dir(out_dir)
            out_file = os.path.join(out_dir, 'index.html')
            
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(output_html)
            
    # Hub Template
    hub_template = env.get_template('hub.html')
    hub_html = hub_template.render(
        page={'title': 'All Articles', 'description': 'Browse all our fleet warranty guides.', 'url': '/articles/'},
        site_name=SITE_NAME,
        site_url=SITE_URL,
        articles=articles,
        current_year=datetime.now(timezone.utc).year
    )
    hub_dir = os.path.join(PUBLIC_DIR, 'articles')
    ensure_dir(hub_dir)
    with open(os.path.join(hub_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(hub_html)

    # Search Template
    search_template = env.get_template('search.html')
    search_html = search_template.render(
        page={'title': 'Search', 'description': 'Search the Extended Car Warranty Hub.', 'url': '/search/'},
        site_name=SITE_NAME,
        site_url=SITE_URL,
        current_year=datetime.now(timezone.utc).year
    )
    search_dir = os.path.join(PUBLIC_DIR, 'search')
    ensure_dir(search_dir)
    with open(os.path.join(search_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(search_html)
        
    with open(os.path.join(PUBLIC_DIR, 'assets', 'search_index.js'), 'w', encoding='utf-8') as f:
        f.write(f"window.searchIndex = {json.dumps(search_index)};")
        
    # Generate Sitemap
    with open(os.path.join(PUBLIC_DIR, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        f.write(f"  <url>\n    <loc>{SITE_URL}/articles/</loc>\n  </url>\n")
        f.write(f"  <url>\n    <loc>{SITE_URL}/search/</loc>\n  </url>\n")
        for item in all_content:
            if item['slug'] != '404':
                loc = urljoin(SITE_URL, item['url'])
                f.write(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{item['last_updated']}</lastmod>\n  </url>\n")
        f.write('</urlset>')

    # Generate RSS
    with open(os.path.join(PUBLIC_DIR, 'rss.xml'), 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
        f.write('<rss version="2.0">\n')
        f.write('  <channel>\n')
        f.write(f'    <title>{SITE_NAME}</title>\n')
        f.write(f'    <link>{SITE_URL}</link>\n')
        f.write(f'    <description>The ultimate resource for commercial vehicle and fleet extended warranties.</description>\n')
        for item in articles[:20]:
            loc = urljoin(SITE_URL, item['url'])
            f.write('    <item>\n')
            f.write(f'      <title>{item["title"]}</title>\n')
            f.write(f'      <link>{loc}</link>\n')
            f.write(f'      <description>{item["description"]}</description>\n')
            try:
                dt = datetime.strptime(item['date'], '%Y-%m-%d')
                pub_date = dt.strftime("%a, %d %b %Y 00:00:00 +0000")
            except:
                pub_date = item['date']
            f.write(f'      <pubDate>{pub_date}</pubDate>\n')
            f.write('    </item>\n')
        f.write('  </channel>\n')
        f.write('</rss>')
        
    # Generate robots.txt
    with open(os.path.join(PUBLIC_DIR, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
        
    print(f"Build complete. Built {len(articles)} articles and {len(pages)} pages to {PUBLIC_DIR}.")

if __name__ == "__main__":
    build_site()
