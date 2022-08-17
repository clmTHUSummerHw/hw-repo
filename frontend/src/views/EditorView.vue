<template>
  <!--TODO: 把编辑器拆分为多个组件，使用vuex共享状态-->
  <div id="editor">
    <el-container id="BOX_BASE">
      <!--最高级容器-->
      <el-header>
        <!--放置-->
        <el-menu
          menu-trigger="click"
          mode="horizontal"
          unique-opened="true"
          @select="handleMenuSelect"
        >
          <!--
                        menu-trigger设置打开子菜单的方式，可供选择还有"hover" /
                        mode属性设horizontal可使其元素水平摆放 / unique-opened=true表示同时只能打开一个子菜单
                        select函数在点击菜单选项时调用
                    -->
          <!--文件栏目-->
          <el-sub-menu index="1">
            <template #title>文件</template>
            <el-menu-item index="1-1">新建文件</el-menu-item>
            <el-menu-item index="1-2">新建文件夹</el-menu-item>
            <el-menu-item index="1-3">删除文件</el-menu-item>
            <el-menu-item index="1-4">删除文件夹</el-menu-item>
          </el-sub-menu>

          <!--编辑栏目-->
          <el-sub-menu index="2">
            <template #title>编辑</template>
            <el-menu-item index="2-1">ele2-1</el-menu-item>
          </el-sub-menu>

          <!--帮助栏目-->
          <el-menu-item>
            <el-link href="README.md">帮助</el-link>
          </el-menu-item>
        </el-menu>
      </el-header>
      <el-container>
        <el-aside id="BOX_PROJECT_FILE_LIST">
          <!--当前项目文件栏-->

          <el-tree
            ref="tree"
            :data="treeData"
            :props="treeProps"
            node-key="id"
            :default-expanded-keys="expandedTreeId"
            @node-click="handleNodeClick"
            highlight-current="true"
          >
            <template #default="{ node, data }">
              <img
                src="~@/assets/icon-folder-close.svg"
                id="folder_close"
                v-if="!node.expanded && data.folder"
              />
              <img
                src="~@/assets/icon-folder-open.svg"
                id="folder_open"
                v-else-if="node.expanded && data.folder"
              />
              <img src="~@/assets/file_type_text.svg" id="file" v-else />
              <span id="label_text">{{ node.label }}</span>
            </template>
          </el-tree>
          <!--展示项目文件夹结构的树形控件-->
        </el-aside>

        <el-main id="BOX_FILE_EDITOR">
          <!--编辑器空间-->
          <el-tabs
            v-model="active_name"
            type="border-card"
            editable
            @edit="handleTabsEdit"
            closable
          >
            <!--editable提供添加tab的按钮 / closable提供可关闭tab的按钮-->

            <!--默认打开的tab，展示向导文件-->
            <el-tab-pane label="WELCOME" name="first">
              WELCOME TAB TO show README DOC
            </el-tab-pane>

            <!--默认提供的编辑器tab-->
            <el-tab-pane label="EDITOR_PAGE" name="second">
              <el-input
                v-model="editorText"
                type="textarea"
                rows="20"
              ></el-input>
            </el-tab-pane>
          </el-tabs>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
//import Node from 'element-plus/es/components/tree/src/model/node' //引入结点类型
import { ElMessage, ElMessageBox } from "element-plus";
import { defineComponent } from "vue";
import axios from "axios";
export default defineComponent({
  name: "EditorView",

  //接受session
  props: {
    session: {
      type: String,
      required: false, //本地项目
      default: "sessionid",
    },
    project: {
      type: String,
      required: false,
      default: "project_name",
    },
  },

  data() {
    return {
      active_index: "1", //目前展开的菜单选项index
      active_name: "", //目前展示的编辑器区域文件名
      treeData: [], //TODO: 抓取并引入项目文件夹结构
      editorText: "", //默认编辑器tab的输入内容
      treeProps: {
        label: "name",
        children: "files",
        isLeaf: "folder",
      },
      expandedTreeId: [1], //key is name,1 is project's treeid
      currentTreeNode: null, //默认是project的treenode
      maxTreeId: 0,
    };
  },
  mounted() {
    setTimeout(() => {
      this.refreshfilelist();
    }, 100);
  },
  methods: {
    getCurrentFilePath(currentTreeNode) {
      var filepath = "";
      if (currentTreeNode["data"]["name"] != this.project) {
        //如果project_name即为根目录"sessionid//projectname//filename"
        filepath =
          filepath + this.getCurrentFilePath(currentTreeNode["parent"]);
        if (currentTreeNode["data"]["folder"] == 1) {
          filepath = currentTreeNode["data"]["name"] + "//";
        }
      }
      return filepath;
    },
    createFile(filename) {
      if (this.currentTreeNode == null) {
        this.currentTreeNode = this.$refs.tree.getNode(1);
      } //如果是null即为根目录project_name
      var filepath = this.getCurrentFilePath(this.currentTreeNode) + filename;
      axios
        .post(
          "http://127.0.0.1:4523/m1/1454888-0-default/project/new-file",
          JSON.stringify({
            session: this.session, //把props里接受session发送到后端
            project: this.project,
            name: filepath,
          })
        )
        .then((resp) => {
          if (resp["data"]["code"] == 0) {
            this.maxTreeId = this.maxTreeId + 1;
            var childdata = {
              name: filename,
              id: this.maxTreeId,
              folder: 0,
            };
            if (this.currentTreeNode["data"]["folder"] == 1) {
              this.$refs.tree.append(childdata, this.currentTreeNode);
            } else {
              this.$refs.tree.append(childdata, this.currentTreeNode["parent"]);
            }
            this.currentTreeNode = this.$refs.tree.getNode(this.maxTreeId);
            this.focusTreeNode(this.currentTreeNode);
            ElMessage({
              type: "success",
              message: `已创建文件:${filename}`,
            });
          } else if (resp["data"]["code"] == 1) {
            alert("session无效");
          } else if (resp["data"]["code"] == 2) {
            alert("项目不存在");
          } else if (resp["data"]["code"] == 3) {
            alert("文件名不符合规范");
          } else if (resp["data"]["code"] == 4) {
            alert("文件已存在");
          } else {
            alert("未知错误");
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    createFolder(foldername) {
      if (this.currentTreeNode == null) {
        this.currentTreeNode = this.$refs.tree.getNode(1);
      }
      var filepath = this.getCurrentFilePath(this.currentTreeNode) + foldername;
      axios
        .post(
          "http://127.0.0.1:4523/m1/1454888-0-default/project/new-folder",
          JSON.stringify({
            session: this.session, //把props里接受session发送到后端
            project: this.project,
            name: filepath,
          })
        )
        .then((resp) => {
          if (resp["data"]["code"] == 0) {
            this.maxTreeId = this.maxTreeId + 1;
            var childdata = {
              name: foldername,
              id: this.maxTreeId,
              folder: 1,
            };
            if (this.currentTreeNode["data"]["folder"] == 1) {
              this.$refs.tree.append(childdata, this.currentTreeNode);
            } else {
              this.$refs.tree.append(childdata, this.currentTreeNode["parent"]);
            }
            this.currentTreeNode = this.$refs.tree.getNode(this.maxTreeId);
            this.focusTreeNode(this.currentTreeNode);
            ElMessage({
              type: "success",
              message: `已创建文件夹:${foldername}`,
            });
          } else if (resp["data"]["code"] == 1) {
            alert("session无效");
          } else if (resp["data"]["code"] == 2) {
            alert("项目不存在");
          } else if (resp["data"]["code"] == 3) {
            alert("文件夹名不符合规范");
          } else if (resp["data"]["code"] == 4) {
            alert("文件夹已存在");
          } else {
            alert("未知错误");
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    createFileMessageBox() {
      ElMessageBox.prompt("Please input your file name", "新建文件", {
        confirmButtonText: "OK",
        cancelButtonText: "Cancel",
        inputPattern: /^[A-Za-z0-9\\.\\_]+$/,
        inputErrorMessage: "请输入正确的文件名",
      })
        .then(({ value }) => {
          this.createFile(value);
        })
        .catch(() => {
          ElMessage({
            type: "info",
            message: "Input canceled",
          });
        });
    },
    createFolderMessageBox() {
      ElMessageBox.prompt("Please input your folder name", "新建文件夹", {
        confirmButtonText: "OK",
        cancelButtonText: "Cancel",
        inputPattern: /^[A-Za-z0-9\\_]+$/,
        inputErrorMessage: "请输入正确的文件夹名",
      })
        .then(({ value }) => {
          this.createFolder(value);
        })
        .catch(() => {
          ElMessage({
            type: "info",
            message: "Input canceled",
          });
        });
    },
    deleteFile() {
      var filepath = this.getCurrentFilePath(this.currentTreeNode);
      axios
        .post(
          "http://127.0.0.1:4523/m1/1454888-0-default/project/delete-file",
          JSON.stringify({
            session: this.session, //把props里接受session发送到后端
            project: this.project,
            name: filepath,
          })
        )
        .then((resp) => {
          if (resp["data"]["code"] == 0) {
            this.$refs.tree.remove(this.currentTreeNode);
            this.currentTreeNode = this.$refs.tree.getNode(1);
            //TODO:删除tap
          } else if (resp["data"]["code"] == 1) {
            alert("session无效");
          } else if (resp["data"]["code"] == 2) {
            alert("项目不存在");
          } else if (resp["data"]["code"] == 3) {
            alert("文件不存在");
          } else if (resp["data"]["code"] == 4) {
            alert("路径为文件夹而非文件");
          } else {
            alert("未知错误");
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    deleteFolder() {
      //不能删项目根目录
      if (this.currentTreeNode["data"]["id"] == 1) {
        alert("不可删除项目根目录");
      } else {
        var filepath = this.getCurrentFilePath(this.currentTreeNode);
        axios
          .post(
            "http://127.0.0.1:4523/m1/1454888-0-default/project/delete-folder",
            JSON.stringify({
              session: this.session, //把props里接受session发送到后端
              project: this.project,
              name: filepath,
            })
          )
          .then((resp) => {
            if (resp["data"]["code"] == 0) {
              this.$refs.tree.remove(this.currentTreeNode);
              //如果是文件夹，还要移除默认展开列表
              var treeIndex = this.expandedTreeId.findIndex((item) => {
                return item == this.currentTreeNode["data"]["id"];
              });
              if (treeIndex != -1) {
                this.expandedTreeId.splice(treeIndex, 1);
              }
              this.currentTreeNode = this.$refs.tree.getNode(1); //只记录不focus
              //TODO:删除tap
            } else if (resp["data"]["code"] == 1) {
              alert("session无效");
            } else if (resp["data"]["code"] == 2) {
              alert("项目不存在");
            } else if (resp["data"]["code"] == 3) {
              alert("文件夹不存在");
            } else if (resp["data"]["code"] == 4) {
              alert("路径为文件而非文件夹");
            } else {
              alert("未知错误");
            }
          })
          .catch(function (error) {
            console.log(error);
          });
      }
    },
    handleMenuSelect(key, keyPath) {
      //应对菜单选择
      //console.log(key);
      if (key == "1-1") {
        this.createFileMessageBox();
      } else if (key == "1-2") {
        this.createFolderMessageBox();
      } else if (key == "1-3") {
        this.deleteFile();
      } else if (key == "1-4") {
        this.deleteFolder();
      }
    },
    /*handleClick(tab, event) {
            //console.log(tab, event);
        },*/
    handleTabsEdit(targetName, action) {
      //应对动态添加/删除tabs，action: 'remove' | 'add'
      if (action === "add") {
        console.log("add!" + targetName);
      } else if (action === "remove") {
        console.log("remove!" + targetName);
      }
    }, //TODO: 定义添加或删除tabs的函数
    focusTreeNode(treenode) {
      this.currentTreeNode = treenode;
      this.$nextTick(() => {
        this.$refs.tree.setCurrentKey(this.currentTreeNode["data"]["id"]);
      });
    },
    handleNodeClick(data, treenode) {
      this.focusTreeNode(treenode);
      if (data["folder"] == 1) {
        //如果是文件夹，加入或移除默认展开列表
        var treeIndex = this.expandedTreeId.findIndex((item) => {
          return item == data["id"];
        });
        if (treeIndex != -1) {
          this.expandedTreeId.splice(treeIndex, 1);
        } else {
          this.expandedTreeId.push(data["id"]);
        }
      }
    },
    addIdPropertyAndSort(tree_arr) {
      function objectSort(firstproperty) {
        return function (Obj1, Obj2) {
          return Obj2[firstproperty] - Obj1[firstproperty];
        };
      } //令文件夹展示在前面
      tree_arr.sort(objectSort("folder"));
      for (var i = 0; i < tree_arr.length; i++) {
        this.maxTreeId = this.maxTreeId + 1;
        tree_arr[i]["id"] = this.maxTreeId;
        if (tree_arr[i]["folder"] == 1) {
          this.addIdPropertyAndSort(tree_arr[i]["files"]);
        }
      }
      return tree_arr;
    },
    refreshfilelist() {
      axios
        .post(
          "http://127.0.0.1:4523/m1/1454888-0-default/project/list-files",
          JSON.stringify({
            session: this.session, //把props里接受session发送到后端
            project: this.project,
          })
        )
        .then((resp) => {
          this.treeData = [];
          if (resp["data"]["code"] == 0) {
            var tree = {};
            this.maxTreeId = 0; //重置treeid，保证project的treeid是1
            tree["name"] = this.project;
            tree["folder"] = 1;
            tree["files"] = resp["data"]["files"];
            this.treeData = this.addIdPropertyAndSort([tree]);
          } else if (resp["data"]["code"] == 1) {
            alert("session无效");
          } else if (resp["data"]["code"] == 2) {
            alert("项目不存在");
          } else {
            alert("未知错误");
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
  },
});
</script>

<style lang="scss">
#editor {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;

  box-sizing: border-box;
  width: 100%;
  height: 800px;

  background-color: white;
  background-image: url(@/assets/small_logo_bg.png);
}

#BOX_BASE {
  /* 整体框 */
  color: black;
  background-color: white;
  box-shadow: 1px 0 10px rgb(0 0 0 / 30%);

  margin: auto;
  width: 90%;
  height: 600px;

  position: relative;
  top: 7%;
}

#BOX_PROJECT_FILE_LIST {
  /* 目前项目文件列表 */
  width: 200px;
  padding: 20px;
  border-right: 1px solid rgb(223, 223, 223);
}

#BOX_FILE_EDITOR {
  /* 编辑器区域 */
  padding: 5px 18px;
}

#folder_close {
  width: 18px;
  height: 18px;
}
#folder_open {
  width: 18px;
  height: 18px;
}
#file {
  width: 18px;
  height: 18px;
}
#label_text {
  //文件名过长显示省略号
  text-overflow: ellipsis;
  overflow: hidden;
}
</style>
