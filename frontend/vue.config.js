const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

module.exports = { //定义入口、模板
  pages: {
    index: {
      entry: "src/pages/index/index.js",
      template: "public/index.html",
      filename: "index.html"
      //title: "",
    },
    editor: {
      entry: "src/pages/editor/editor.js",
      template: "public/editor.html",
      filename: "editor.html"
    },
    projectList: {
      entry: "src/pages/projectList/projectList.js",
      template: "public/projectList.html",
      filename: "projectList.html"
    },
    signUp: {
      entry: "src/pages/signUp/signUp.js",
      template: "public/signUp.html",
      filename: "signUp.html"
    }
  },
  //lintOnSave: false //关闭eslint提示
}