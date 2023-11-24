import { useState } from "react";
import "./App.css";
import React from "react";
import axios from "axios";
import {
    Form,
    Input,
    Button,
    message,
    Space,
    Layout,
    Card,
    Typography,
} from "antd";
import {useNavigate} from "react-router-dom";

const baseurl = "https://6cbpmuhemh.execute-api.us-east-2.amazonaws.com/dev/";

function Register() {
    const [messageApi, contextHolder] = message.useMessage(); // 页面上方提示话框
    const [form_register] = Form.useForm();
    const {Title} = Typography;
    let navigate = useNavigate();
    return (
        <>
            {contextHolder}
            <Layout style={{ minHeight: "100vh", display: "grid", placeItems: "center", background: "#9DCD84" }}>
                <Card style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', width: "600px"}}>
                    <Space direction="vertical" size="small" style={{ display: "flex" }}>
                        <Title level={3} style={{fontFamily: 'Dancing Script'}}>
                            Register
                        </Title>
                        <div style={{ width: '50px' }} />
                        <div style={{ width: '50px' }} />
                        <Form form={form_register} name="basic" labelCol={{ span: 8 }} style={{ maxWidth: 600 }} initialValues = {{ remember: true }} autoComplete = "off">
                            <Form.Item label = {
                                <span style = {{ fontSize: 14, fontFamily: 'Orbitron', width: '200px'}}>
                              Username
                            </span>
                            } name = "username" rules = {[{ required: true, message: "Please input your userName!" }]}>
                                <Input />
                            </Form.Item>

                            <Form.Item label = {
                                <span style = {{ fontSize: 14, fontFamily: 'Orbitron', width: '200px'}}>
                              Password
                            </span>
                            } name = "Password" rules = {[{ required: true, message: "Please input your password!" }]}>
                                <Input.Password />
                            </Form.Item>

                            <Space direction="horizontal">
                                <Form.Item wrapperCol={{ offset: 10, span: 16 }}>
                                    <Button htmlType="submit" type="primary" style={{ width: 120, fontFamily: 'Orbitron'}} onClick={()=>{
                                            if (form_register.getFieldValue("username") != null && form_register.getFieldValue("Password") != null) {
                                                axios.get(`${baseurl}getUserInfo?UserName=${form_register.getFieldValue("username")}`, {
                                                    headers: {
                                                        "x-api-key": "urLOROFoXZC3weFVmAmV7l5QtbEMOi67kBBr9UI8"
                                                    }
                                                }).then((response) => {
                                                    messageApi.info("The username has been already used.");
                                                }).catch(error => {
                                                    if (form_register.getFieldValue("Password").length < 8) {
                                                        messageApi.info(
                                                            "The password is too short. (Required at least 8 letters)"
                                                        );
                                                    } else {
                                                        axios.post(`${baseurl}userInsert`, {
                                                            "Password": form_register.getFieldValue("Password"),
                                                            "UserName": form_register.getFieldValue("username"),
                                                        }, {
                                                            headers: {
                                                                "x-api-key": "urLOROFoXZC3weFVmAmV7l5QtbEMOi67kBBr9UI8"
                                                            }
                                                        }).catch(error => {
                                                            messageApi.info(
                                                                "Please input your information."
                                                            );
                                                        });
                                                        navigate('/Login');
                                                    }
                                                });
                                            }
                                        }
                                    }>
                                        Register
                                    </Button>
                                </Form.Item>

                                <Form.Item wrapperCol={{ offset: 18, span: 16 }}>
                                    <Button htmlType="submit" type="primary" style={{ width: 120, fontFamily: 'Orbitron' }} onClick={()=>{ navigate('/Login'); }}>
                                        Back To Log
                                    </Button>
                                </Form.Item>
                            </Space>
                        </Form>
                    </Space>
                </Card>
            </Layout>
        </>
    );
}

export default Register;

