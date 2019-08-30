module.exports = {
  TREEHERDER_URL: 'https://treeherder.mozilla.org',
  TASKCLUSTER_TOOLS_URL: 'https://tools.taskcluster.net',
  AUTH0: {
    domain: 'auth.mozilla.auth0.com',
    clientID: 'FK1mJkHhwjulTYBGklxn8W4Fhd1pgT4t',
    redirectUri: new URL('/login', window.location).href,
    scope: 'full-user-credentials openid profile email',
  },
  PRODUCTS: [
    {
      product: 'firefox',
      prettyName: 'Firefox Desktop',
      appName: 'browser',
      branches: [
        {
          prettyName: 'Maple Beta',
          project: 'maple',
          branch: 'projects/maple',
          repo: 'https://hg.mozilla.org/projects/maple',
          enableReleaseEta: true,
        },
        {
          prettyName: 'Try',
          project: 'try',
          branch: 'try',
          repo: 'https://hg.mozilla.org/try',
          enableReleaseEta: false,
        },
      ],
      enablePartials: false,
    },
    {
      product: 'fennec',
      prettyName: 'Firefox Mobile',
      // TODO: The actual appName is `mobile/android` but it gets the version from `browser`.
      appName: 'browser',
      branches: [
        {
          prettyName: 'Maple Beta',
          project: 'maple',
          branch: 'projects/maple',
          repo: 'https://hg.mozilla.org/projects/maple',
          enableReleaseEta: false,
          alternativeBranch: 'releases/mozilla-beta',
        },
        {
          prettyName: 'Try',
          project: 'try',
          branch: 'try',
          repo: 'https://hg.mozilla.org/try',
          enableReleaseEta: false,
        },
        {
          prettyName: 'Try Beta',
          project: 'maple',
          branch: 'try',
          repo: 'https://hg.mozilla.org/try',
          enableReleaseEta: false,
          productKey: 'fennec_beta',
          versionFile: 'mobile/android/config/version-files/beta/version_display.txt',
        },
        {
          prettyName: 'Try Release',
          project: 'maple',
          branch: 'try',
          repo: 'https://hg.mozilla.org/try',
          enableReleaseEta: false,
          productKey: 'fennec_release',
          versionFile: 'mobile/android/config/version-files/release/version_display.txt',
        },
      ],
      enablePartials: false,
    },
    {
      product: 'devedition',
      prettyName: 'Firefox Developer Edition',
      appName: 'browser',
      branches: [
        {
          prettyName: 'Maple Beta',
          project: 'maple',
          branch: 'projects/maple',
          repo: 'https://hg.mozilla.org/projects/maple',
          enableReleaseEta: false,
        },
        {
          prettyName: 'Try',
          project: 'try',
          branch: 'try',
          repo: 'https://hg.mozilla.org/try',
          enableReleaseEta: false,
        },
      ],
      enablePartials: true,
    },
    {
      product: 'thunderbird',
      prettyName: 'Thunderbird',
      appName: 'mail',
      branches: [
        {
          prettyName: 'Try',
          project: 'try-comm-central',
          branch: 'try-comm-central',
          repo: 'https://hg.mozilla.org/try-comm-central',
          enableReleaseEta: false,
        },
      ],
      // TODO
      enablePartials: false,
    },
  ],
};
