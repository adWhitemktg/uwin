import {defineArrayMember, defineField, defineType} from 'sanity'

export const faq = defineType({
  name: 'faq',
  title: 'FAQ',
  type: 'document',
  fields: [
    defineField({
      name: 'question',
      title: 'Question',
      type: 'string',
      validation: (rule) => rule.required(),
    }),
    defineField({
      name: 'answer',
      title: 'Answer',
      type: 'text',
      rows: 5,
      validation: (rule) => rule.required(),
    }),
    defineField({
      name: 'topic',
      title: 'Topic',
      type: 'string',
      options: {
        list: [
          {title: 'Service', value: 'service'},
          {title: 'Service Area', value: 'serviceArea'},
          {title: 'Material', value: 'material'},
          {title: 'Style', value: 'style'},
          {title: 'Financing', value: 'financing'},
          {title: 'Installation', value: 'installation'},
          {title: 'Warranty', value: 'warranty'},
          {title: 'General', value: 'general'},
        ],
      },
    }),
    defineField({
      name: 'relatedMaterials',
      title: 'Related Materials',
      type: 'array',
      of: [
        defineArrayMember({
          type: 'reference',
          to: [{type: 'windowMaterial'}],
        }),
      ],
    }),
    defineField({
      name: 'relatedStyles',
      title: 'Related Styles',
      type: 'array',
      of: [
        defineArrayMember({
          type: 'reference',
          to: [{type: 'windowStyle'}],
        }),
      ],
    }),
    defineField({
      name: 'relatedServiceAreas',
      title: 'Related Service Areas',
      type: 'array',
      of: [
        defineArrayMember({
          type: 'reference',
          to: [{type: 'serviceArea'}],
        }),
      ],
    }),
    defineField({
      name: 'schemaEligible',
      title: 'Schema Eligible',
      type: 'boolean',
      initialValue: true,
    }),
    defineField({
      name: 'lastReviewed',
      title: 'Last Reviewed',
      type: 'date',
    }),
  ],
  preview: {
    select: {
      title: 'question',
      subtitle: 'topic',
    },
  },
})
