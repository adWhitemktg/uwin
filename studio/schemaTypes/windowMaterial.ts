import {defineArrayMember, defineField, defineType} from 'sanity'

export const windowMaterial = defineType({
  name: 'windowMaterial',
  title: 'Window Material',
  type: 'document',
  fields: [
    defineField({
      name: 'name',
      title: 'Name',
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
      name: 'summary',
      title: 'Summary',
      type: 'text',
      rows: 4,
    }),
    defineField({
      name: 'benefits',
      title: 'Benefits',
      type: 'array',
      of: [defineArrayMember({type: 'string'})],
    }),
    defineField({
      name: 'tradeoffs',
      title: 'Drawbacks / Tradeoffs',
      type: 'text',
      rows: 3,
    }),
    defineField({
      name: 'bestFor',
      title: 'Best For',
      type: 'text',
      rows: 3,
    }),
    defineField({
      name: 'energyNotes',
      title: 'Energy Notes',
      type: 'text',
      rows: 3,
    }),
    defineField({
      name: 'compatibleStyles',
      title: 'Compatible Styles',
      type: 'array',
      of: [
        defineArrayMember({
          type: 'reference',
          to: [{type: 'windowStyle'}],
        }),
      ],
    }),
    defineField({
      name: 'relatedFaqs',
      title: 'Related FAQs',
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
  ],
  preview: {
    select: {
      title: 'name',
      subtitle: 'summary',
    },
  },
})
