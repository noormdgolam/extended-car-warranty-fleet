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

    import random
    
    spin_intros = [
        f"Protecting your commercial vehicles is essential for maintaining business operations. In this article, we dive deep into **{title}**.",
        f"Fleet managers know that vehicle downtime directly impacts profitability. That's why understanding **{title}** is a critical component of risk management for any modern business.",
        f"When a crucial vehicle breaks down, the costs extend far beyond the repair shop bill. Today, we're exploring **{title}** to help you keep your operations running smoothly and predictably."
    ]
    
    spin_bodies = [
        "### What is Typically Covered?\nMost comprehensive commercial warranties cover the critical components that keep your fleet moving. This includes the Engine and Transmission, Drive Axle assemblies, Electrical Components (which are increasingly complex in modern vehicles), and Heating/Cooling Systems. Ensuring these are protected under a commercial use policy is paramount.\n\n### What is Excluded?\nAlways read the fine print! Common exclusions in fleet warranties include routine maintenance like oil changes, brake pads, and tires. Additionally, any damage resulting from accidents, driver misuse, or unauthorized repairs will void the claim. \n\n## Cost vs Benefit\n\nIs an extended warranty worth the upfront premium? Let's break down the economics. On average, a major transmission repair on a commercial vehicle can cost upwards of $4,000 to $6,000. If an extended warranty costs $1,500 per vehicle per year, the peace of mind and financial predictability often outweigh the premium, especially when managing multiple assets.",
        "### Core Coverage Details\nWhen negotiating a fleet warranty, you must prioritize the powertrain. The engine block, turbochargers, transmission, and drivetrain are the most expensive parts to replace. Secondary systems like suspension, steering, and AC are also vital for driver comfort and safety. \n\n### Common Pitfalls and Exclusions\nMany business owners fail to realize that standard consumer warranties explicitly exclude commercial use. If you use a vehicle for deliveries or trades, you need a specific commercial endorsement. Exclusions always apply to wear-and-tear items (wipers, belts, hoses) and any aftermarket modifications not approved by the manufacturer.\n\n## The Financial Calculation\n\nFleet maintenance is a numbers game. A single catastrophic engine failure can wipe out a month's profit for a small business. While setting aside a cash reserve for repairs is one strategy, an extended fleet warranty provides a fixed, predictable cost that can be easily budgeted and often written off as a business expense.",
        "### Standard Commercial Inclusions\nA robust fleet warranty should offer bumper-to-bumper or stated-component coverage. This means protection for the engine, transmission, transfer case, and electrical systems. Advanced plans also cover emissions systems, which are notoriously expensive to fix on modern diesel trucks.\n\n### What You Pay For Out of Pocket\nRemember that an extended warranty is a service contract against defect and failure, not a maintenance plan. You will still be responsible for fluid changes, filters, brake rotors, and alignments. Failure to perform these routine tasks according to the manufacturer's schedule can actually void your warranty coverage.\n\n## Why Fleet Managers Choose Warranties\n\nPredictability is the lifeblood of logistics and service businesses. While premium costs add to the overhead, they prevent the massive capital shocks associated with major repairs. Furthermore, many commercial warranties include towing and substitute vehicle coverage, minimizing the operational disruption when a breakdown occurs."
    ]
    
    spin_faqs = [
        "**Q: Can I use any repair shop?**\nA: Many third-party warranty providers allow you to use any ASE-certified mechanic, but always verify their network requirements before signing the contract.\n\n**Q: Do fleet warranties cover roadside assistance?**\nA: Yes, the best commercial plans include 24/7 heavy-duty roadside assistance, towing to the nearest authorized facility, and sometimes even rental vehicle reimbursement.",
        "**Q: Are these warranties transferable if I sell the vehicle?**\nA: In most cases, yes. Transferring a commercial warranty to the new owner can significantly increase the resale value of your fleet vehicle, though a small administrative fee may apply.\n\n**Q: How are claims processed?**\nA: Usually, the repair facility contacts the warranty administrator directly to get authorization before beginning work. You only pay your agreed-upon deductible.",
        "**Q: What is a typical deductible for a commercial warranty?**\nA: Deductibles usually range from $100 to $500. Some providers offer a 'disappearing deductible' if you use their preferred nationwide repair network.\n\n**Q: Is there a waiting period before coverage starts?**\nA: Typically, yes. Most contracts have a 30-day and 1,000-mile waiting period to prevent pre-existing condition claims."
    ]
    
    intro_text = random.choice(spin_intros)
    body_text = random.choice(spin_bodies)
    faq_text = random.choice(spin_faqs)

    content = f"""---
title: "{title}"
description: "Comprehensive guide to {title}. Learn how to protect your fleet, manage costs, and keep your business vehicles on the road."
keyword: "{keyword}"
author: "Fleet Protection Expert"
date: "{pub_date}"
slug: "{slug}"
---

{intro_text}

## Key Takeaways
- Fleet warranties reduce unpredictable repair costs.
- Ensure your specific vehicle type is covered under commercial use terms.
- Compare deductibles, coverage limits, and repair networks.

## Understanding Coverage Options

{body_text}

## Frequently Asked Questions (FAQ)

{faq_text}
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
