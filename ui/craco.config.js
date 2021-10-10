const CracoLessPlugin = require('craco-less');
const AntdDayjsWebpackPlugin = require('antd-dayjs-webpack-plugin');

module.exports = {
  plugins: [
    {
      plugin: CracoLessPlugin,
      options: {
        lessLoaderOptions: {
          lessOptions: {
            modifyVars: { '@primary-color': '#9D2133' },
            javascriptEnabled: true,
          },
        },
      },
    },
    {
      plugin: new AntdDayjsWebpackPlugin(),
    },
  ],
};
