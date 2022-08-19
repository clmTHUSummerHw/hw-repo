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
            <el-menu-item index="1-3">上传文件</el-menu-item>
            <el-menu-item index="1-4">下载文件</el-menu-item>
            <el-menu-item index="1-5">保存文件</el-menu-item>
            <el-menu-item index="1-6">删除</el-menu-item>
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
      <el-container id="content">
        <el-aside id="BOX_PROJECT_FILE_LIST">
          <div class="uploadhide">
            <el-upload
              ref="upload"
              :auto-upload="false"
              :on-change="uploadFile"
              :show-file-list="false"
            >
              <template #trigger>
                <el-button type="primary" class="uploadButton"
                  >select file</el-button
                >
              </template>
            </el-upload>
          </div>
          <el-menu
            mode="vertical"
            v-show="menuVisible"
            class="contextmenu"
            @select="handleContextmenu"
          >
            <el-menu-item index="1">新建文件</el-menu-item>
            <el-menu-item index="2">新建文件夹</el-menu-item>
            <!--包括删除文件和删除文件夹-->
            <el-menu-item index="3">删除</el-menu-item>
            <el-menu-item index="4">下载文件</el-menu-item>
          </el-menu>
          <!--当前项目文件栏-->
          <el-tree
            ref="tree"
            :data="treeData"
            :props="treeProps"
            node-key="id"
            :default-expanded-keys="expandedTreeId"
            @node-click="handleNodeClick"
            highlight-current="true"
            @node-contextmenu="handleNodeContextmenu"
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
            @tab-change="handleTabChange"
            closable
          >
            <!--editable提供添加tab的按钮 / closable提供可关闭tab的按钮-->
            <el-tab-pane
              v-for="item in editableTabs"
              :key="item.name"
              :label="item.title"
              :name="item.name"
            >
              <el-input v-model="item.content" type="textarea" rows="20">
              </el-input>
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
      active_name: "first", //目前展示的编辑器区域文件名(tap_name)
      editableTabs: [
        {
          title: "WELCOME",
          name: "first",
          content: "WELCOME TAB TO show README DOC",
        },
        {
          title: "EDITOR_PAGE",
          name: "second",
          content: "EDITOR_PAGE content",
        },
      ], //打开的所有tap,title与文件名关联，name与文件的id关联
      editorText: "", //默认编辑器tab的输入内容

      treeData: [], //TODO: 抓取并引入项目文件夹结构
      treeProps: {
        label: "name",
        children: "files",
        isLeaf: "folder",
      },
      expandedTreeId: [1], //key is name,1 is project's treeid
      currentTreeNode: null, //默认是project的treenode
      maxTreeId: 0,
      menuVisible: false,
      ContextmenuNode: null, //右键菜单选择的节点
    };
  },
  mounted() {
    setTimeout(() => {
      this.refreshfilelist();
    }, 100);
  },
  methods: {
    uploadFile(file, fileList) {
      this.getBase64(file.raw).then((result) => {
        var currentTreeNode = this.currentTreeNode;
        if (currentTreeNode == null) {
          currentTreeNode = this.$refs.tree.getNode(1);
        } //如果是null即为根目录project_name
        var filepath = this.getCurrentFilePath(currentTreeNode) + file["name"];
        axios
          .post(
            "http://127.0.0.1:4523/m1/1454888-0-default/project/upload-file",
            JSON.stringify({
              session: this.session, //把props里接受session发送到后端
              project: this.project,
              name: filepath,
              file: result,
            })
          )
          .then((resp) => {
            if (resp["data"]["code"] == 0) {
              this.maxTreeId = this.maxTreeId + 1;
              var childdata = {
                name: file["name"],
                id: this.maxTreeId,
                folder: 0,
              };
              if (currentTreeNode["data"]["folder"] == 1) {
                this.$refs.tree.append(childdata, currentTreeNode);
              } else {
                this.$refs.tree.append(childdata, currentTreeNode["parent"]);
              }
              this.focusTreeNode(this.$refs.tree.getNode(this.maxTreeId));
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
      });
    },
    getBase64(file) {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      let result = "";
      return new Promise(function (resolve, reject) {
        reader.onload = function () {
          result = reader.result.split(",")[1];
        };
        reader.onloadend = function () {
          resolve(result);
        };
      });
    },
    downloadFile(currentTreeNode) {
      if (currentTreeNode == null) {
        alert("请选择要下载的文件");
      } else if (currentTreeNode["data"]["folder"] == 1) {
        alert("暂不支持下载文件夹");
      } else {
        var filepath =
          this.getCurrentFilePath(currentTreeNode) +
          currentTreeNode["data"]["name"];
        axios
          .post(
            "http://127.0.0.1:4523/m1/1454888-0-default/project/download-file",
            JSON.stringify({
              session: this.session, //把props里接受session发送到后端
              project: this.project,
              name: filepath,
            })
          )
          .then((resp) => {
            if (resp["data"]["code"] == 0) {
              var elementA = document.createElement("a"); // 创建a标签
              elementA.download = currentTreeNode["data"]["name"]; //文件的名称
              elementA.style.display = "none";
              var blob = new Blob([atob(resp["data"]["file"])]); //生成一个blob二进制数据，内容为从后端获得的文件内容
              elementA.href = URL.createObjectURL(blob);
              document.body.appendChild(elementA);
              elementA.click();
              document.body.removeChild(elementA);
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
      }
    },
    getCurrentFilePath(currentTreeNode) {
      var filepath = "";
      if (
        currentTreeNode != null &&
        currentTreeNode["data"]["name"] != this.project
      ) {
        //如果project_name即为根目录"sessionid//projectname//filename"
        filepath =
          filepath + this.getCurrentFilePath(currentTreeNode["parent"]);
        if (currentTreeNode["data"]["folder"] == 1) {
          filepath = currentTreeNode["data"]["name"] + "//";
        }
      }
      return filepath;
    },
    createFile(currentTreeNode, filename) {
      if (currentTreeNode == null) {
        currentTreeNode = this.$refs.tree.getNode(1);
      } //如果是null即为根目录project_name
      var filepath = this.getCurrentFilePath(currentTreeNode) + filename;
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
            if (currentTreeNode["data"]["folder"] == 1) {
              this.$refs.tree.append(childdata, currentTreeNode);
            } else {
              this.$refs.tree.append(childdata, currentTreeNode["parent"]);
            }
            this.focusTreeNode(this.$refs.tree.getNode(this.maxTreeId));
            //在右侧新增tab
            this.addTab(filename, `${this.maxTreeId}`, "");
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
    createFolder(currentTreeNode, foldername) {
      if (currentTreeNode == null) {
        currentTreeNode = this.$refs.tree.getNode(1);
      }
      var filepath = this.getCurrentFilePath(currentTreeNode) + foldername;
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
            if (currentTreeNode["data"]["folder"] == 1) {
              this.$refs.tree.append(childdata, currentTreeNode);
            } else {
              this.$refs.tree.append(childdata, currentTreeNode["parent"]);
            }
            this.focusTreeNode(this.$refs.tree.getNode(this.maxTreeId));
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
    createFileMessageBox(currentTreeNode) {
      ElMessageBox.prompt("Please input your file name", "新建文件", {
        confirmButtonText: "OK",
        cancelButtonText: "Cancel",
        inputPattern: /^[A-Za-z0-9\\.\\_]+$/,
        inputErrorMessage: "请输入正确的文件名",
      })
        .then(({ value }) => {
          this.createFile(currentTreeNode, value);
        })
        .catch(() => {
          ElMessage({
            type: "info",
            message: "Input canceled",
          });
        });
    },
    createFolderMessageBox(currentTreeNode) {
      ElMessageBox.prompt("Please input your folder name", "新建文件夹", {
        confirmButtonText: "OK",
        cancelButtonText: "Cancel",
        inputPattern: /^[A-Za-z0-9\\_]+$/,
        inputErrorMessage: "请输入正确的文件夹名",
      })
        .then(({ value }) => {
          this.createFolder(currentTreeNode, value);
        })
        .catch(() => {
          ElMessage({
            type: "info",
            message: "Input canceled",
          });
        });
    },
    deleteFile(currentTreeNode) {
      var filepath = this.getCurrentFilePath(currentTreeNode);
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
            this.$refs.tree.remove(currentTreeNode);
            this.currentTreeNode = this.$refs.tree.getNode(1);
            this.editableTabs.forEach((tab) => {
              if (tab.title === currentTreeNode["data"]["name"]) {
                this.removeTab(tab.name);
              }
            }); //如果之前已打开tab，还要删除tab
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
    deleteFolder(currentTreeNode) {
      //不能删项目根目录
      if (currentTreeNode["data"]["id"] == 1) {
        alert("不可删除项目根目录");
      } else {
        var filepath = this.getCurrentFilePath(currentTreeNode);
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
              this.$refs.tree.remove(currentTreeNode);
              //如果是文件夹，还要移除默认展开列表
              var treeIndex = this.expandedTreeId.findIndex((item) => {
                return item == currentTreeNode["data"]["id"];
              });
              if (treeIndex != -1) {
                this.expandedTreeId.splice(treeIndex, 1);
              }
              this.currentTreeNode = this.$refs.tree.getNode(1); //只记录不focus
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
    saveFile(currentTreeNode) {
      if (currentTreeNode == null) {
        alert("请选择要保存的文件");
      } else {
        var pane = document.getElementById(`pane-${this.active_name}`);
        var filecontent = pane.getElementsByTagName("textarea")[0].value;
        var filepath =
          this.getCurrentFilePath(currentTreeNode) +
          currentTreeNode["data"]["name"];
        axios
          .post(
            "http://127.0.0.1:4523/m1/1454888-0-default/project/upload-file",
            JSON.stringify({
              session: this.session, //把props里接受session发送到后端
              project: this.project,
              name: filepath,
              file: filecontent,
            })
          )
          .then((resp) => {
            if (resp["data"]["code"] == 0) {
              ElMessage({
                type: "success",
                message: "保存成功",
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
      }
    },
    handleMenuSelect(key, keyPath) {
      //应对菜单选择
      if (key == "1-1") {
        this.createFileMessageBox(this.currentTreeNode);
      } else if (key == "1-2") {
        this.createFolderMessageBox(this.currentTreeNode);
      } else if (key == "1-3") {
        document.querySelector(".uploadButton").click();
      } else if (key == "1-4") {
        this.downloadFile(this.currentTreeNode);
      } else if (key == "1-5") {
        this.saveFile(this.currentTreeNode);
      } else if (key == "1-6") {
        if (this.currentTreeNode["data"]["folder"] == 1) {
          this.deleteFolder(this.currentTreeNode);
        } else {
          this.deleteFile(this.currentTreeNode);
        }
      }
    },
    handleContextmenu(key, keyPath) {
      if (key == "1") {
        this.createFileMessageBox(this.ContextmenuNode);
      } else if (key == "2") {
        this.createFolderMessageBox(this.ContextmenuNode);
      } else if (key == "3") {
        if (this.ContextmenuNode["data"]["folder"] == 1) {
          this.deleteFolder(this.ContextmenuNode);
        } else {
          this.deleteFile(this.ContextmenuNode);
        }
      } else if (key == "4") {
        this.downloadFile(this.ContextmenuNode);
      }
    },
    handleTabsEdit(targetName, action) {
      //应对动态添加/删除tabs，action: 'remove' | 'add'
      if (action === "add") {
        console.log("add!" + targetName);
      } else if (action === "remove") {
        this.removeTab(targetName);
      }
    }, //TODO: 定义添加或删除tabs的函数
    handleTabChange() {
      //改变tab的同时改变currentTreeNode并聚焦，使两者关联，便于保存文件的实现
      this.focusTreeNode(this.$refs.tree.getNode(this.active_name));
    },
    addTab(tabtitle, tabname, tabcontent) {
      this.editableTabs.push({
        title: tabtitle,
        name: tabname,
        content: tabcontent,
      });
      this.active_name = tabname;
    },
    removeTab(tabname) {
      if (this.active_name === tabname) {
        this.editableTabs.forEach((tab, index) => {
          if (tab.name === tabname) {
            var nextTab =
              this.editableTabs[index + 1] || this.editableTabs[index - 1];
            if (nextTab) {
              this.active_name = nextTab.name;
            } else {
              this.active_name = null;
            }
          }
        });
      }
      this.editableTabs = this.editableTabs.filter(
        (tab) => tab.name !== tabname
      );
    },
    focusTreeNode(treenode) {
      this.currentTreeNode = treenode;
      this.$nextTick(() => {
        if (this.currentTreeNode == null) {
          this.$refs.tree.setCurrentKey(null);
        } else {
          this.$refs.tree.setCurrentNode(this.currentTreeNode);
        }
      });
    },
    openFile(treenode) {
      var findtab = false;
      this.editableTabs.forEach((tab) => {
        if (tab.title === treenode["data"]["name"]) {
          this.active_name = tab.name;
          findtab = true;
        }
      });
      if (!findtab) {
        var filepath =
          this.getCurrentFilePath(treenode) + treenode["data"]["name"];
        axios
          .post(
            "http://127.0.0.1:4523/m1/1454888-0-default/project/download-file",
            JSON.stringify({
              session: this.session, //把props里接受session发送到后端
              project: this.project,
              name: filepath,
            })
          )
          .then((resp) => {
            if (resp["data"]["code"] == 0) {
              this.addTab(
                treenode["data"]["name"],
                `${treenode["data"]["id"]}`,
                atob(resp["data"]["file"])
              );
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
      }
    },
    handleNodeClick(data, treenode) {
      //应对点击节点
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
      } else {
        //如果是文件，新增或打开右侧编辑器的tab，title和文件名相同
        this.openFile(treenode);
      }
    },
    hideContextmenu() {
      // 取消鼠标监听事件 菜单栏
      this.menuVisible = false;
      this.ContextmenuNode = null;
      document.removeEventListener("click", this.hideContextmenu); // 关掉监听，
    },
    handleNodeContextmenu(event, data, treenode) {
      //应对右键点击节点
      this.menuVisible = false; // 先把模态框关死，为了多次点击右键时菜单能随鼠标移动
      this.menuVisible = true; // 显示模态窗口，跳出自定义菜单栏
      this.ContextmenuNode = treenode;
      event.preventDefault(); //关闭浏览器右键默认事件
      let menu = document.querySelector(".contextmenu");
      /* 菜单定位基于鼠标点击位置 */
      menu.style.left = event.clientX - 100 + "px";
      menu.style.top = event.clientY - 60 + "px";
      document.addEventListener("click", this.hideContextmenu);
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
//自定义图标
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
//右键菜单
#BOX_PROJECT_FILE_LIST > .el-menu {
  position: absolute;
  background-color: #fff;
  width: 120px;
  /*height: 106px;*/
  font-size: 10px;
  color: #444040;
  border-radius: 4px;
  -webkit-box-sizing: border-box;
  box-sizing: border-box;
  border-radius: 3px;
  border: 1px solid rgba(0, 0, 0, 0.15);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.175);
  white-space: nowrap;
  z-index: 1000;
}
#BOX_PROJECT_FILE_LIST > .el-menu > .el-menu-item {
  display: block;
  line-height: 34px;
  text-align: left;
}
#BOX_PROJECT_FILE_LIST > .el-menu > .el-menu-item:not(:last-child) {
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}
#BOX_PROJECT_FILE_LIST > .el-menu > .el-menu-item:hover {
  cursor: pointer;
  background: #66b1ff;
  border-color: #66b1ff;
  color: #fff;
}
.uploadhide {
  display: none;
}
</style>
