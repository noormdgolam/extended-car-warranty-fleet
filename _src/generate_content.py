import os
from datetime import datetime, timedelta

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

base_dir = os.path.dirname(os.path.abspath(__file__))
content_dir = os.path.join(base_dir, 'content')

ensure_dir(os.path.join(content_dir, 'articles'))
ensure_dir(os.path.join(content_dir, 'pages'))
ensure_dir(os.path.join(content_dir, 'legal'))

# Generate legal pages
legal_pages = {
    "about": {"title": "About Us", "desc": "Learn about the Extended Car Warranty Hub for Fleet Owners."},
    "contact": {"title": "Contact Us", "desc": "Get in touch with our commercial fleet warranty experts."},
    "privacy-policy": {"title": "Privacy Policy", "desc": "Our privacy policy and cookie usage details for Google AdSense compliance."},
    "terms": {"title": "Terms of Service", "desc": "Terms and conditions for using our website."},
    "disclaimer": {"title": "Disclaimer", "desc": "Important disclaimer regarding our warranty information."}
}

for slug, meta in legal_pages.items():
    content = f"""---
title: "{meta['title']}"
description: "{meta['desc']}"
author: "Editorial Team"
date: "2024-01-01"
slug: "{slug}"
---

# {meta['title']}

Welcome to our {meta['title']} page. 

*Placeholder content for {meta['title']}. Make sure to update this with real information before launch.*
"""
    with open(os.path.join(content_dir, 'legal', f'{slug}.md'), 'w', encoding='utf-8') as f:
        f.write(content)

# Fleet warranty topics (100+ total articles)
vehicle_types = ["Delivery Vans", "Heavy Duty Trucks", "Light Commercial Vehicles", "Box Trucks", "Sprinter Vans", "Company Cars", "Utility Trucks", "Refrigerated Trucks", "Passenger Vans", "Step Vans"]
industries = ["Plumbing", "HVAC", "Delivery and Logistics", "Landscaping", "Construction", "Catering", "Cleaning Services", "Electricians", "Pest Control", "Sales Teams"]
states = ["California", "Texas", "Florida", "New York", "Pennsylvania", "Illinois", "Ohio", "Georgia", "North Carolina", "Michigan"]

print("Generating 100+ Articles...")
start_date = datetime(2023, 1, 1)

for i in range(110):
    if i < 40:
        vt = vehicle_types[i % len(vehicle_types)]
        ind = industries[(i // 4) % len(industries)] # staggered
        title = f"Extended Car Warranty for {vt} in the {ind} Industry"
        keyword = f"{vt} extended warranty"
    elif i < 80:
        st = states[(i - 40) % len(states)]
        vt = vehicle_types[((i - 40) // 4) % len(vehicle_types)] # staggered
        title = f"Best Commercial Fleet Warranty for {vt} in {st}"
        keyword = f"fleet warranty {st}"
    else:
        topic = [
            "Cost-Benefit Analysis of Fleet Warranties",
            "How to Negotiate Commercial Warranty Rates",
            "What Does a Powertrain Fleet Warranty Cover?",
            "Bumper-to-Bumper vs Powertrain for Fleets",
            "Managing Claims for Multiple Fleet Vehicles",
            "Are Extended Fleet Warranties Tax Deductible?",
            "Top 5 Pitfalls to Avoid in Fleet Warranties",
            "Maintenance Requirements for Fleet Warranties",
            "Transferring Fleet Warranties when Selling Vehicles",
            "OEM vs Third-Party Extended Fleet Warranties",
            "Top Mistakes When Buying Fleet Protection",
            "Fleet Warranty Costs in 2024",
            "How to Cancel a Fleet Warranty",
            "Comparing Extended Warranties for Fleet Operations",
            "Do Commercial Trucks Need Extended Warranties?"
        ][(i - 80) % 15]
        st = states[((i - 80) // 2) % len(states)]
        title = f"{topic} ({st} Edition)"
        keyword = f"fleet warranties guide"

    slug = title.lower().replace(" ", "-").replace(",", "").replace(":", "").replace("(", "").replace(")", "").replace("?", "")
    pub_date = (start_date + timedelta(days=i*3)).strftime("%Y-%m-%d")

    content = f"""---
title: "{title}"
description: "Comprehensive guide to {title}. Learn how to protect your fleet, manage costs, and keep your business vehicles on the road."
keyword: "{keyword}"
author: "Fleet Protection Expert"
date: "{pub_date}"
slug: "{slug}"
---

Protecting your commercial vehicles is essential for maintaining business operations. In this article, we dive deep into **{title}**.

## Key Takeaways
- Fleet warranties reduce unpredictable repair costs.
- Ensure your specific vehicle type is covered under commercial use terms.
- Compare deductibles and coverage limits.

## Understanding Coverage Options

When managing a fleet, unexpected breakdowns can ruin your profit margins. An extended warranty acts as a financial safety net. 

### What is Typically Covered?
Most comprehensive commercial warranties cover:
- Engine and Transmission
- Drive Axle
- Electrical Components
- Heating and Cooling Systems

### What is Excluded?
Always read the fine print! Common exclusions include:
- Routine maintenance (oil changes, brakes, tires)
- Damage from accidents or misuse
- Unauthorized repairs

## Cost vs Benefit

Is an extended warranty worth it? Let's break down the costs. On average, a major transmission repair on a commercial vehicle can cost upwards of $4,000. If an extended warranty costs $1,500 per vehicle per year, the peace of mind and financial predictability often outweigh the premium.

## Frequently Asked Questions (FAQ)

**Q: Can I use any repair shop?**
A: Many third-party warranty providers allow you to use any ASE-certified mechanic, but always verify their network requirements.

**Q: Do fleet warranties cover roadside assistance?**
A: Yes, the best plans include 24/7 commercial roadside assistance, towing, and sometimes even rental vehicle reimbursement.
"""
    with open(os.path.join(content_dir, 'articles', f'{slug}.md'), 'w', encoding='utf-8') as f:
        f.write(content)

index_content = """---
title: "Extended Car Warranty Hub for Fleet Owners"
description: "The ultimate resource for commercial vehicle and fleet extended warranties. Compare options, save money, and keep your business moving."
keyword: "fleet extended warranty"
author: "Fleet Protection Expert"
date: "2024-01-01"
slug: "index"
---

Welcome to the **Extended Car Warranty Hub**. We specialize in providing the most accurate, up-to-date information for businesses looking to protect their vehicle fleets. 

Whether you manage a handful of delivery vans or a massive fleet of heavy-duty trucks, unexpected repair costs can destroy your bottom line. We review the best commercial warranty plans, break down the costs, and guide you on how to negotiate the best rates.
"""
with open(os.path.join(content_dir, 'index.md'), 'w', encoding='utf-8') as f:
    f.write(index_content)

not_found_content = """---
title: "404 - Page Not Found"
description: "The page you are looking for could not be found."
author: "Admin"
date: "2024-01-01"
slug: "404"
---

# Page Not Found

We couldn't find the page you were looking for. Please try using our search function or return to the [homepage](/).
"""
with open(os.path.join(content_dir, '404.md'), 'w', encoding='utf-8') as f:
    f.write(not_found_content)

print("Done generating placeholder content.")
