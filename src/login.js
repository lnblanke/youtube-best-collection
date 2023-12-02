import "./App.css";
import React from "react";
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
import { NavLink, useNavigate} from "react-router-dom";
import axios from "axios";

const baseurl = "https://6cbpmuhemh.execute-api.us-east-2.amazonaws.com/prod/";

const Login = () => {
    const [messageApi, contextHolder] = message.useMessage(); // 页面上方提示话框
    const [form_login] = Form.useForm();
    const {Title} = Typography;
    let navigate = useNavigate();
    return (
        <>
            {contextHolder}
            <Layout style={{ minHeight: "100vh", display: "grid", placeItems: "center", background: "#9DCD84" }}>
                <Card style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', width: "600px", background: "#FFFFFF" }}>
                    <Space direction="vertical" size="small" style={{ display: "flex"}}>
                        <Space direction="horizontal" size="small" style={{ display: "flex"}}>
                            <div style={{width:'50px'}}></div>
                            <Title level={3} style={{fontFamily: 'Dancing Script', margin: '20px',display: "flex"}}>
                                Welcome to Youtube Best Collection
                            </Title>
                        </Space>
                        <div style={{ width: '50px' }} />
                        <div style={{ width: '50px' }} />
                        <Form form={form_login} name="basic" labelCol={{ span: 8 }} style={{ maxWidth: 600 }} initialValues = {{ remember: true }} autoComplete = "off">
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
                                    <Button htmlType="submit" type="primary" style={{ width: 120, fontFamily: 'Orbitron'}}  onClick = {() => {
                                        axios.get(`${baseurl}getUserInfo?UserName=${form_login.getFieldValue("username")}`,{
                                            headers: {
                                                "x-api-key": "urLOROFoXZC3weFVmAmV7l5QtbEMOi67kBBr9UI8"
                                            }
                                        }).then((response)=>{
                                            const userName_temp = form_login.getFieldValue("username");
                                            if (response.data['data'][0]['Password'] === form_login.getFieldValue("Password")) {
                                                navigate('/Home', { state: { data: userName_temp } });
                                            } else {
                                                messageApi.info("The password is wrong, please try again.");
                                            }
                                        }).catch(error=> {
                                                messageApi.info("User does not EXIST. Please try again.");
                                            }
                                        );
                                    }}>
                                        Log In
                                    </Button>
                                </Form.Item>

                                <Form.Item wrapperCol={{ offset: 18, span: 16 }}>
                                    <Button htmlType="submit" type="primary" style={{ width: 120, fontFamily: 'Orbitron'}} onClick={()=>{ navigate('/Register') }}>
                                        Sign Up
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

export default Login;

