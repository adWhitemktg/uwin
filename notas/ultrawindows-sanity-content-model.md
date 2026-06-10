# Ultra Windows Sanity Content Model

## 1. Model Goal

The goal is to model the durable business entities behind Ultra Windows, not to recreate the current WordPress page structure one page at a time.

Sanity should become the database and editor for the business system:

```text
Business
├── Services
├── Service Areas
├── Window Materials
├── Window Styles
├── Projects
├── Testimonials
├── FAQs
├── Offers / Financing
├── Articles
└── Landing Pages
```

The current site has many pages that are really different presentations of the same underlying entities. For example, a city page, an aluminum-in-city page, a footer link, a FAQ, and a testimonial may all be talking about the same service area, material, and offer. The content model should make those relationships explicit.

Most important rule:

```text
Do not model current pages.
Model the business entities that current pages are trying to describe.
```

Pages can then be generated from structured records where possible.

## 2. Document Types

Recommended first-pass document types:

- `siteSettings`
- `service`
- `serviceArea`
- `windowMaterial`
- `windowStyle`
- `project`
- `testimonial`
- `faq`
- `offer`
- `article`
- `landingPage`
- `redirectOrQuarantine`

These types separate durable content from page output. A service area is a business entity. A window material is a business entity. A testimonial is proof. A landing page is only a composed presentation of those entities.

## 3. Fields Per Document Type

### `siteSettings`

- Business name
- Logo
- Phone
- Address
- Social links
- Primary CTA
- Footer navigation
- Global SEO defaults

### `service`

- Name, for example `Replacement Windows`
- Slug
- Overview
- Benefits
- Process
- Warranty notes
- Related FAQs
- Related testimonials
- Related projects

### `serviceArea`

- City/community name
- Slug
- State
- County/region
- Intro
- Local considerations
- Available services
- Available materials
- Available styles
- Nearby areas
- Featured projects
- Featured testimonials
- Area FAQs
- SEO title
- SEO description
- Old URLs / redirect notes

### `windowMaterial`

- Name, for example Aluminum, Vinyl, Fiberglass, Composite, Wood Clad
- Slug
- Summary
- Benefits
- Drawbacks/tradeoffs
- Best for
- Not best for
- Colors/options
- Energy notes
- Compatible styles
- Related projects
- Related FAQs
- SEO fields

### `windowStyle`

- Name, for example Casement, Double Hung, Single Hung, Picture, Sliding, Garden, Bay/Bow
- Slug
- Summary
- Best for
- Ventilation notes
- Visual notes
- Compatible materials
- Related projects
- Related FAQs
- SEO fields

### `project`

- Title
- Slug
- City/service area
- Materials used
- Styles used
- Project type
- Before images
- After images
- Install notes
- Customer quote/testimonial
- Review source
- Publish status

### `testimonial`

- Headline
- Quote/body
- Customer name or initials
- City/service area
- Rating
- Source
- Related project
- Related material
- Related style
- Permission/status

### `faq`

- Question
- Answer
- Topic
- Related service
- Related material
- Related style
- Related service area
- Schema eligible
- Last reviewed

### `offer`

- Offer name
- Financing provider
- Summary
- Terms
- Disclaimer
- Eligibility
- CTA
- Start date
- End date

### `article`

- Title
- Slug
- Publish date
- Excerpt
- Body
- Category/topic
- Related services
- Related materials
- Related styles
- Related service areas
- Related FAQs

### `landingPage`

- Title
- Slug
- Page purpose
- Sections/modules
- Referenced entities
- SEO fields

### `redirectOrQuarantine`

- Old URL
- New target URL
- Action: redirect / noindex / 410 / quarantine
- Reason
- Notes

## 4. References Between Documents

The relationships are more important than the fields. The model should make these relationships easy to manage:

```text
serviceArea → services
serviceArea → materials
serviceArea → styles
serviceArea → projects
serviceArea → testimonials
serviceArea → FAQs

material → styles
material → projects
material → FAQs

style → materials
style → projects
style → FAQs

project → serviceArea
project → materials
project → styles
project → testimonial

article → related entities
faq → related entities
```

Practical examples:

- A `serviceArea` record for Tomball can reference Replacement Windows, Aluminum, Vinyl, Casement, local projects, and relevant testimonials.
- A `windowMaterial` record for Aluminum can reference compatible styles like Casement, Picture, Sliding, and related FAQs.
- A `project` can connect proof to a location, a material, a style, and a testimonial.
- A `faq` can appear on the global FAQ page, a material page, a style page, and a service area page without duplicating content.
- An `article` can support internal linking by referencing the entities it discusses.

## 5. Page Templates Generated From Documents

Sanity should support generated page templates where the page is mostly a view of structured entities.

Recommended generated templates:

- Home page: generated from `siteSettings`, core `service`, proof modules, offers, and selected landing sections.
- Service page: generated from `service` plus related materials, styles, FAQs, projects, testimonials, and offers.
- Service area page: generated from `serviceArea` plus referenced services, materials, styles, projects, testimonials, and FAQs.
- Material page: generated from `windowMaterial` plus compatible styles, projects, FAQs, and service CTA.
- Style page: generated from `windowStyle` plus compatible materials, projects, FAQs, and service CTA.
- Project/proof page: generated from `project` records and external Project Map It dependency, if retained.
- Testimonials page: generated from `testimonial` records.
- FAQ page: generated from `faq` records grouped by topic.
- Financing page: generated from `offer` records.
- Article pages: generated from `article` records.
- Landing pages: manually composed from sections/modules and referenced entities.

The current site has many pages that should probably become generated templates instead of individually authored pages.

## 6. Legacy URL Decisions

Legacy URLs should be reviewed as their own migration data, not mixed into the main content model.

Recommended actions:

- Keep canonical URLs for strong pages that map cleanly to a business entity.
- Redirect merged service-area/material/style pages to the best canonical generated page.
- Noindex or quarantine suspicious resource pages before deciding whether to redirect them.
- Use `410` for pages that should be removed and have no legitimate replacement.
- Track every old URL in `redirectOrQuarantine` with a reason and action.

Likely legacy groups:

- Core pages: homepage, replacement windows, about, contact, financing.
- Service area pages: city/community replacement window pages.
- Material pages: aluminum, vinyl, fiberglass, composite, wood clad.
- Style pages: casement, double hung, single hung, picture, sliding, garden, bay/bow.
- Proof pages: projects and testimonials.
- Articles: blog/advice content.
- Suspicious pages: `610xxxx` resource pages and pages with unrelated outbound links.

## 7. What Not To Migrate

Do not migrate these as ordinary content pages:

- Machine-generated `610xxxx` resource pages.
- Pages whose main purpose is unrelated outbound linking.
- Duplicate city pages that only swap a location name without meaningful local content.
- Material-plus-location pages unless they have real local proof or unique demand.
- Footer/navigation lists as body content.
- Repeated CTA blocks as page-specific content.
- Repeated financing blurbs as page-specific content.
- Repeated FAQ answers copied into many pages.
- Review/testimonial headings without the underlying quote/body, attribution, rating, or permission status.

These should become structured data, redirects, reusable modules, or quarantined legacy records.

## 8. Open Questions

- Which URLs are business-critical enough to preserve exactly?
- Which `610xxxx` pages are indexed, receiving traffic, or attracting backlinks?
- Does Ultra Windows want separate city pages for every service area, or a smaller set of strong regional pages?
- Which service areas have real projects, photos, testimonials, or local proof?
- Are aluminum and fiberglass location-specific pages worth keeping, or should material availability live inside service-area records?
- What is the correct business start year to use everywhere? Current content appears to reference multiple "since" years.
- What is the canonical business address and service radius?
- Which testimonials have permission to republish, and which have customer names, initials, ratings, or source URLs?
- Should Project Map It remain the project source of truth, or should projects be migrated into Sanity?
- What financing details are current, and what terms/disclaimers are required?
- Which FAQs have approved answers, and when were they last reviewed?
- Who owns content review for warranty, financing, and claims about energy efficiency?
