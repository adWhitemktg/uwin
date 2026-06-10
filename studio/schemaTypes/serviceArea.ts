import {defineArrayMember, defineField, defineType} from 'sanity'

export const serviceArea = defineType({
  name: 'serviceArea',
  title: 'Service Area',
  type: 'document',
  fields: [
    defineField({
      name: 'name',
      title: 'City / Community Name',
      type: 'string',
      validation: (rule) => rule.required(),
    }),
    defineField({
      name: 'slug',
      title: 'Slug',
      type: 'slug',
      options: {source: 'name', maxLength: 96},
      validation: (rule) => rule.required(),
    }),
    defineField({
      name: 'state',
      title: 'State',
      type: 'string',
      initialValue: 'Texas',
    }),
    defineField({
      name: 'region',
      title: 'County / Region',
      type: 'string',
    }),
    defineField({
      name: 'intro',
      title: 'Intro',
      type: 'text',
      rows: 4,
    }),
    defineField({
      name: 'localConsiderations',
      title: 'Local Considerations',
      type: 'text',
      rows: 4,
    }),
    defineField({
      name: 'availableMaterials',
      title: 'Available Materials',
      type: 'array',
      of: [
        defineArrayMember({
          type: 'reference',
          to: [{type: 'windowMaterial'}],
        }),
      ],
    }),
    defineField({
      name: 'availableStyles',
      title: 'Available Styles',
      type: 'array',
      of: [
        defineArrayMember({
          type: 'reference',
          to: [{type: 'windowStyle'}],
        }),
      ],
    }),
    defineField({
      name: 'nearbyAreas',
      title: 'Nearby Areas',
      type: 'array',
      of: [
        defineArrayMember({
          type: 'reference',
          to: [{type: 'serviceArea'}],
        }),
      ],
    }),
    defineField({
      name: 'areaFaqs',
      title: 'Area FAQs',
      type: 'array',
      of: [
        defineArrayMember({
          type: 'reference',
          to: [{type: 'faq'}],
        }),
      ],
    }),
    defineField({
      name: 'seoTitle',
      title: 'SEO Title',
      type: 'string',
    }),
    defineField({
      name: 'seoDescription',
      title: 'SEO Description',
      type: 'text',
      rows: 3,
    }),
    defineField({
      name: 'legacyUrls',
      title: 'Old URLs / Redirect Notes',
      type: 'array',
      of: [
        defineArrayMember({
          type: 'object',
          fields: [
            defineField({name: 'url', title: 'Old URL', type: 'url'}),
            defineField({
              name: 'notes',
              title: 'Notes',
              type: 'text',
              rows: 2,
            }),
          ],
          preview: {
            select: {title: 'url', subtitle: 'notes'},
          },
        }),
      ],
    }),
  ],
  preview: {
    select: {
      title: 'name',
      subtitle: 'region',
    },
  },
})
