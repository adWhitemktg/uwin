import {defineCliConfig} from 'sanity/cli'

export default defineCliConfig({
  api: {
    projectId: 'w1f4v4do',
    dataset: 'production'
  },
  deployment: {
    autoUpdates: false,
  }
})
