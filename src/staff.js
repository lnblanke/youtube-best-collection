import { useState } from "react";
import React from "react";
import {
  Modal,
  Form,
  Space,
  Table,
  Input,
  DatePicker,
  Upload,
  message,
  Select,
  Button,
  Checkbox,
  Layout,
  Menu,
  Drawer,
  Card,
} from "antd";
import axios from "axios";
import FormConsist from "./form.js";
import PropTypes from "prop-types";
import {
  SearchOutlined,
  AppstoreOutlined,
  HomeOutlined,
  InboxOutlined,
  UnorderedListOutlined,
  UserOutlined,
  PlusCircleOutlined,
  MinusOutlined
} from "@ant-design/icons";

const baseURL = "http://192.168.187.167:8000/";

const { Header, Content, Sider } = Layout;
const items1 = [
  {
    label: "Current Information",
    key: "get",
    icon: <HomeOutlined />,
  },
  {
    label: "Upload Information",
    key: "post",
    icon: <AppstoreOutlined />,
  },
  {
    label: "Upload Excel",
    key: "upload",
    icon: <InboxOutlined />,
  },
  {
    label: "Order",
    key: "order",
    icon: <UnorderedListOutlined />,
  },
  {
    label: "Search",
    key: "search",
    icon: <SearchOutlined />,
  },
  {
    label: "User",
    key: "user",
    icon: <UserOutlined />,
  },
]; //菜单

function Staff(prop) {
  const columns = [
    {
      title: "Badge",
      dataIndex: "badge",
      key: "badge",
    },
    {
      title: "Name",
      dataIndex: "name",
      key: "name",
    },
    {
      title: "Name_English",
      dataIndex: "name_en",
      key: "name_en",
    },
    {
      title: "E-mail",
      dataIndex: "email",
      key: "email",
    },
    {
      title: "JoinTime",
      dataIndex: "jointime",
      key: "jointime",
    },
    {
      title: "Bu",
      dataIndex: "bu",
      key: "bu",
    },
    {
      title: "Dept",
      dataIndex: "dept",
      key: "dept",
    },
    {
      title: "Action",
      key: "action",
      render: (_, record) => (
        <Space size="middle">
          <a
            onClick={() => {
              showModal(record);
            }}
          >
            Alter{" "}
          </a>

          <a
            onClick={() => {
              setBadge_inline(record.badge);
              setIsModalOpen_del(true);
            }}
          >
            Delete
          </a>
        </Space>
      ),
    },
  ]; //表格框架
  const [get, setGet] = React.useState(null); //主表格显示
  const [get_search, setGet_search] = React.useState(null); //搜索栏特殊表格
  const [isModalOpen, setIsModalOpen] = useState(false); //更改数据时弹出的窗口
  const [isModalOpen_del, setIsModalOpen_del] = useState(false); //删除数据时的窗口确认
  const [isModalOpen_post, setIsModalOpen_post] = useState(false); //上传数据时弹出的窗口
  const [isModalOpen_upload, setIsModalOpen_upload] = useState(false); //上传Excel时弹出的窗口
  const [isModalOpen_clear, setIsModalOpen_clear] = useState(false); //清空数据时弹出的窗口
  const [bad, setBad] = useState(false); //单行的Badge
  const [current, setCurrent] = useState("get"); //菜单当前所指
  const [geT, setG] = useState(get); //最终显示的表格
  const [menu, setMenu] = useState(1); //判断下端是否存在搜索框
  const [badge_inline, setBadge_inline] = useState(null); //删除时寻找的badge
  const [clearDecision, setclearDecision] = useState(false); //checkbox确认删除
  const [form] = Form.useForm(); //主表格
  const [form_2] = Form.useForm(); //search
  const [form_3] = Form.useForm(); //order
  const informValue = Form.useWatch("search", form_2); //search搜索栏动态监视
  const dateValue = Form.useWatch("date", form_2); //日期动态监视
  const [openDrawer, setOpenDrawer] = useState(false);
  const [lastKey, setLastKey] = useState("get"); //上传操作前的key
  const [items2, setItems2] = useState([]); //用户栏
  const [numUser, setNumUser] = useState([]); //用户栏
  const [currentUser, setCurrentUser] = useState(); //当前用户

  const onClick = (e) => {
    if (e.key == "get") {
      setLastKey(current);
      setCurrent(e.key);
      setG(get);
      setMenu(1);
    }
    if (e.key == "post") {
      setLastKey(current);
      setCurrent(e.key);
      setIsModalOpen_post(true);
    }
    if (e.key == "upload") {
      setLastKey(current);
      setCurrent(e.key);
      setIsModalOpen_upload(true);
    }
    if (e.key == "search") {
      setLastKey(current);
      setCurrent(e.key);
      setG(get_search);
      setMenu(2);
    }
    if (e.key == "order") {
      setLastKey(current);
      setCurrent(e.key);
      setMenu(3);
    }
    if (e.key == "user") {
      setLastKey(current);
      setCurrent(e.key);
      setOpenDrawer(true);
    }
  }; //菜单切换

  const showModal = (record) => {
    setBad(record.badge);
    setIsModalOpen(true);
  }; //开post

  const handleOk = async () => {
    await axios.put(`${baseURL}${currentUser}/${bad}`, {
      name: form.getFieldValue("name"),
      name_en: form.getFieldValue("name_en"),
      email: form.getFieldValue("email"),
      jointime: form.getFieldValue("jointime"),
      bu: form.getFieldValue("bu"),
      dept: form.getFieldValue("dept"),
    });
    axios.get(`${baseURL}${currentUser}/`).then((response) => {
      setGet(response.data);
      form.resetFields();
      setIsModalOpen(false);
    });
  }; //Alter

  const handleOk_post = async () => {
    await axios.post(`${baseURL}${currentUser}/information/`, {
      badge: form.getFieldValue("badge"),
      name: form.getFieldValue("name"),
      name_en: form.getFieldValue("name_en"),
      email: form.getFieldValue("email"),
      jointime: form.getFieldValue("jointime"),
      bu: form.getFieldValue("bu"),
      dept: form.getFieldValue("dept"),
    });
    axios.get(`${baseURL}${currentUser}/`).then((response) => {
      setGet(response.data);
      form.resetFields();
      setCurrent(lastKey);
      setIsModalOpen_post(false);
    });
  }; //Post

  const handleCancel = () => {
    form.resetFields();
    setIsModalOpen(false);
  }; //关闭Alter窗口

  const handleCancel_post = () => {
    form.resetFields();
    setIsModalOpen_post(false);
    setCurrent(lastKey);
  }; //关闭Post窗口

  const dele_Ok = async () => {
    axios.delete(`${baseURL}${currentUser}/${badge_inline}`).then(() => {
      axios.get(`${baseURL}${currentUser}/`).then((response) => {
        setGet(response.data);
      });
    });
    setIsModalOpen_del(false);
  }; //关闭Delete窗口

  const onPriorityChange = (value) => {
    switch (value) {
      case "badge":
        axios.get(`${baseURL}${currentUser}/order/badge`).then((response) => {
          setG(response.data);
        });
        break;
      case "name":
        axios.get(`${baseURL}${currentUser}/order/name`).then((response) => {
          setG(response.data);
        });
        break;
      case "name_en":
        axios.get(`${baseURL}${currentUser}/order/name_en`).then((response) => {
          setG(response.data);
        });
        break;
      case "email":
        axios.get(`${baseURL}${currentUser}/order/email`).then((response) => {
          setG(response.data);
        });
        break;
      case "jointime":
        axios
          .get(`${baseURL}${currentUser}/order/jointime`)
          .then((response) => {
            setG(response.data);
          });
        break;
      case "dept":
        axios.get(`${baseURL}${currentUser}/order/dept`).then((response) => {
          setG(response.data);
        });
        break;
      case "bu":
        axios.get(`${baseURL}${currentUser}/order/bu`).then((response) => {
          setG(response.data);
        });
        break;
      default:
        break;
    }
  }; //更改order需求

  const onOk_clear = () => {
    axios.delete(`${baseURL}${currentUser}/`).then(() => {
      axios.get(`${baseURL}${currentUser}/`).then((response) => {
        setGet(response.data);
      });
    });
    setIsModalOpen_clear(false);
  }; //clear确认

  const cancel_Ok = () => {
    setIsModalOpen_del(false);
    setIsModalOpen_upload(false);
    setIsModalOpen_clear(false);
    setCurrent(lastKey);
  }; //关闭窗口

  const add_User = () => {
    const item = numUser.map((icon, index) => {
      const key = String(index + 1);
      return {
        key: `user${key}`,
        icon: React.createElement(icon),
        label: `File ${key}`,
      };
    });
    axios.post(`${baseURL}user${numUser.length}/`);
    setItems2(item);
  };

  React.useEffect(() => {
    (async () => {
      axios.get(baseURL).then((response) => {
        for (var i = 0; i < response.data - 1; i++) {
          if (numUser.length < response.data - 1) {
            numUser.push(UserOutlined);
          }
        }
        const item = numUser.map((icon, index) => {
          const key = String(index + 1);
          return {
            key: `user${key}`,
            icon: React.createElement(icon),
            label: `File ${key}`,
          };
        });
        setItems2(item);
      });
    })();
  }, []); //用户栏
  React.useMemo(() => {
    if (currentUser) {
      axios
        .get(
          `${baseURL}${currentUser}/${
            informValue || dateValue?.format("YYYY-MM-DD") || ""
          }?date=${dateValue?.format("YYYY-MM-DD") || ""}`
        )
        .then((response) => {
          setGet_search(response.data);
          setG(response.data);
        });
    }
  }, [currentUser, informValue, dateValue, get]); //search表格变化

  const { Dragger } = Upload;
  const props = {
    name: "file",
    multiple: false,
    action: `http://192.168.187.167:8000/${currentUser}/upload/`,
    onChange(info) {
      const { status } = info.file;
      if (status === "done") {
        message.success(`${info.file.name} file uploaded successfully.`);
        axios.get(`${baseURL}${currentUser}/`).then((response) => {
          setGet(response.data);
        });
      } else if (status === "error") {
        message.error(`${info.file.name} file upload failed.`);
      }
    },
  }; //上传

  return (
    <>
      <Layout>
        <Header style={{ background: "#E4F2E7" }}>
          <div className="demo-logo" />
          <Menu
            mode="horizontal"
            defaultOpenKeys="get"
            onClick={onClick}
            selectedKeys={current}
            items={items1}
            style={{
              justifyContent: "space-evenly",
              padding: "0px 100px",
              background: "#E4F2E7",
            }}
          />
        </Header>
        <Layout>
          <Sider width={200} style={{ background: "#E4F2E7" }}>
            <p></p>
            <Space direction="vertical" align="start">
              <Space direction="horizontal">
                <Button
                  onClick={() => {
                    numUser.push(UserOutlined);
                    add_User();
                  }}
                  style={{ width: 50, background: "#AEFFFA" }}
                >
                  <PlusCircleOutlined />
                </Button>
                <Button
                  onClick={() => {
                    axios.delete(`${baseURL}user${numUser.length}/information/all/`);
                    numUser.pop();
                    const item = numUser.map((icon, index) => {
                      const key = String(index + 1);
                      return {
                        key: `user${key}`,
                        icon: React.createElement(icon),
                        label: `File ${key}`,
                      };
                    });
                    setItems2(item);
                  }}
                  style={{ width: 50 }}
                  danger
                >
                  <MinusOutlined />
                </Button>
              </Space>
              <Menu
                mode="inline"
                style={{ background: "#E4F2E7" }}
                items={items2}
                onClick={(e) => {
                  setCurrentUser(e.key);
                }}
              />
            </Space>
          </Sider>
          <Layout>
            <Content
              style={{
                padding: 30,
                margin: 0,
                minHeight: 300,
                background: "#EEF4F0",
              }}
            >
              <Card>
                <Space
                  direction="vertical"
                  size="large"
                  style={{ display: "flex" }}
                >
                  {currentUser ? (
                    <Table
                      columns={columns}
                      dataSource={geT}
                      rowKey="badge"
                      pagination={{ hideOnSinglePage: true }}
                    />
                  ) : null}

                  {menu == 1 || menu == 3 || currentUser == null ? null : (
                    <Form form={form_2} layout="vertical" autoComplete="off">
                      <Form.Item name="search">
                        <Input placeholder="请输入你想要查询的信息" />
                      </Form.Item>

                      <Form.Item name="date">
                        <DatePicker />
                      </Form.Item>
                    </Form>
                  )}

                  {menu == 1 || menu == 2 || currentUser == null ? null : (
                    <Form form={form_3} layout="vertical" autoComplete="off">
                      <Form.Item
                        name="order"
                        label="Order"
                        rules={[
                          {
                            required: true,
                          },
                        ]}
                      >
                        <Select
                          placeholder="Select a option as the first priority"
                          onChange={onPriorityChange}
                          allowClear
                        >
                          <option value="badge">Badge</option>
                          <option value="name">Name</option>
                          <option value="name_en">Name in English</option>
                          <option value="email">E-mail</option>
                          <option value="jointime">Jointime</option>
                          <option value="bu">Bu</option>
                          <option value="dept">Dept</option>
                        </Select>
                      </Form.Item>
                    </Form>
                  )}
                  {currentUser ? (
                    <Button
                      onClick={() => {
                        setIsModalOpen_clear(true);
                      }}
                      danger
                    >
                      Clear
                    </Button>
                  ) : null}
                </Space>
              </Card>
            </Content>
          </Layout>
        </Layout>
      </Layout>
      <FormConsist
        put_or_post={true}
        form={form}
        isModalOpen={isModalOpen}
        handleOk={handleOk}
        handleCancel={handleCancel}
      />
      <FormConsist
        put_or_post={false}
        form={form}
        isModalOpen={isModalOpen_post}
        handleOk={handleOk_post}
        handleCancel={handleCancel_post}
      />
      <Modal
        title="Are you sure to delete?"
        open={isModalOpen_del}
        onOk={dele_Ok}
        onCancel={cancel_Ok}
      ></Modal>
      <Modal
        title="Upload Your Excel"
        open={isModalOpen_upload}
        footer={null}
        onCancel={cancel_Ok}
      >
        <Dragger {...props}>
          <p className="ant-upload-drag-icon">
            <InboxOutlined />
          </p>
          <p className="ant-upload-text">上传Excel文档</p>
          <p className="ant-upload-hint">这只是一个测试，请上传Excel文档</p>
        </Dragger>
      </Modal>
      <Modal
        title="Clear Decision"
        open={isModalOpen_clear}
        onOk={onOk_clear}
        onCancel={cancel_Ok}
        okButtonProps={{ disabled: !clearDecision }}
      >
        <p>Please consider if you decide to CLEAR ALL the information. </p>
        <Checkbox
          checked={clearDecision}
          onChange={(e) => setclearDecision(e.target.checked)}
        >
          Yes, I'm sure.
        </Checkbox>
      </Modal>

      <Drawer
        title="User Information"
        placement="right"
        onClose={() => {
          setCurrent(lastKey);
          setOpenDrawer(false);
        }}
        open={openDrawer}
        style={{ background: "#DEF5EA" }}
      >
        <Space direction="vertical" align="start" size="middle">
          {/*<p style={{ fontSize: "15px" }}>*/}
          {/*  {" "}*/}
          {/*  Current User: {prop.form.getFieldValue("username")}{" "}*/}
          {/*</p>*/}
          <Button
            onClick={() => {
              prop.login(1);
              if (prop.rem == false) {
                prop.form.resetFields();
              }
            }}
            danger
          >
            Log Out
          </Button>
        </Space>
      </Drawer>
    </>
  );
}

Staff.propTypes = {
  form: PropTypes.object,
  login: PropTypes.func,
  rem: PropTypes.bool,
};
export default Staff;
