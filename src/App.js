import { useState } from "react";
import "./App.css";
import React from "react";
import axios from "axios";
import {
  Form,
  Input,
  Button,
  Checkbox,
  message,
  Space,
  Layout,
  Typography,
  Image,
  Card,
} from "antd";
import Staff from "./staff.js";

const baseURL = "http://192.168.187.167:8000/";

function login() {
  // eslint-disable-next-line react-hooks/rules-of-hooks
  const [login, setLogin] = useState(1);
  // eslint-disable-next-line react-hooks/rules-of-hooks
  const [form] = Form.useForm();
  // eslint-disable-next-line react-hooks/rules-of-hooks
  const [form1] = Form.useForm();
  // eslint-disable-next-line react-hooks/rules-of-hooks
  const [rem, setRem] = useState(false);
  const [messageApi, contextHolder] = message.useMessage();

  return (
    <>
      {contextHolder}
      {!(login == 1) ? null : (
        <Layout
          style={{
            minHeight: "100vh",
            display: "grid",
            placeItems: "center",
            background: "#E4F2E7",
          }}
        >
          <Card style={{width: 700}}>
            <Space
              direction="vertical"
              size="small"
              style={{ display: "flex" }}
            >
              <p style={{ fontSize: "35px" }}>
                Dealer
              </p>
              <Form
                form={form}
                name="basic"
                labelCol={{
                  span: 8,
                }}
                wrapperCol={{
                  span: 16,
                }}
                style={{
                  maxWidth: 600,
                }}
                initialValues={{
                  remember: true,
                }}
                autoComplete="off"
              >
                <Form.Item
                  label={
                    <span style={{ fontSize: 15 }}>
                      Username
                    </span>
                  }
                  name="username"
                  rules={[
                    {
                      required: true,
                      message: "Please input your username!",
                    },
                  ]}
                >
                  <Input />
                </Form.Item>

                <Form.Item
                  label={
                    <span style={{ fontSize: 15 }}>
                      Password
                    </span>
                  }
                  name="password"
                  rules={[
                    {
                      required: true,
                      message: "Please input your password!",
                    },
                  ]}
                >
                  <Input.Password />
                </Form.Item>

                <Form.Item
                  name="remember"
                  wrapperCol={{
                    offset: 4,
                    span: 16,
                  }}
                >
                  <Checkbox
                    onChange={(e) => {
                      setRem(e.target.checked);
                    }}
                  >
                    Remember me
                  </Checkbox>
                </Form.Item>

                <Space direction="horizontal">
                  <Form.Item
                    wrapperCol={{
                      offset: 13,
                      span: 16,
                    }}
                  >
                    <Button
                      htmlType="submit"
                      type="primary"
                      style={{width: 150}}
                      onClick={() => {
                        axios
                          .get(
                            `${baseURL}users/login/${form.getFieldValue(
                              "username"
                            )}/${form.getFieldValue("password")}`
                          )
                          .then((response) => {
                            if (response.data == 1) {
                              setLogin(2);
                            } else {
                              messageApi.info(
                                "The username or password is wrong, please try again."
                              );
                              form.resetFields();
                            }
                          });
                      }}
                    >
                      Log in
                    </Button>
                  </Form.Item>
                  <Form.Item
                    wrapperCol={{
                      offset:15,
                      span: 16,
                    }}
                  >
                    <Button
                      onClick={() => {
                        setLogin(3);
                      }}
                      style={{width: 150}}
                    >
                      Register
                    </Button>
                  </Form.Item>
                </Space>
              </Form>
            </Space>
          </Card>
        </Layout>
      )}
      {!(login == 2) ? null : (
        <>
          <Staff form={form} login={setLogin} rem={rem} />
        </>
      )}
      {!(login == 3) ? null : (
        <Form
          form={form1}
          name="basic"
          labelCol={{
            span: 8,
          }}
          wrapperCol={{
            span: 16,
          }}
          style={{
            maxWidth: 600,
          }}
          initialValues={{
            remember: true,
          }}
        >
          <Form.Item
            label="Username"
            name="username"
            rules={[
              {
                required: true,
                message: "Please input your username!",
              },
            ]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="Password"
            name="password"
            rules={[
              {
                required: true,
                message: "Please input your password!",
              },
            ]}
          >
            <Input.Password />
          </Form.Item>

          <Form.Item
            wrapperCol={{
              offset: 8,
              span: 16,
            }}
          >
            <Button
              onClick={() => {
                axios
                  .get(`${baseURL}users/login/${form1.getFieldValue("username")}`)
                  .then((response) => {
                    if (response.data == 1) {
                      messageApi.info("The username has been already used.");
                    } else if (
                      form1.getFieldValue("username") == null ||
                      form1.getFieldValue("password").length == null
                    ) {
                      messageApi.info(
                        "Please input your username or password."
                      );
                    } else if (form1.getFieldValue("username").length < 3) {
                      messageApi.info(
                        "The username is too short. (Required at least 3 letters)"
                      );
                    } else if (form1.getFieldValue("password").length < 6) {
                      messageApi.info(
                        "The password is too short. (Required at least 6 letters)"
                      );
                    } else {
                      axios.post(
                        `${baseURL}users/register/${form1.getFieldValue(
                          "username"
                        )}/${form1.getFieldValue("password")}`
                      );
                      messageApi.info("User successfully Created");
                      setLogin(1);
                    }
                    form1.resetFields();
                  });
              }}
            >
              Register
            </Button>
          </Form.Item>

          <Form.Item
            wrapperCol={{
              offset: 8,
              span: 16,
            }}
          >
            <Button
              onClick={() => {
                setLogin(1);
              }}
            >
              Back to Log
            </Button>
          </Form.Item>
        </Form>
      )}
    </>
  );
}

export default login;
