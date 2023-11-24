import "./App.css";
import React, {useState} from "react";
import ImgCrop from 'antd-img-crop';
import {
    Table,
    Layout,
    Card,
    Input,
    Space,
    Typography,
    Radio,
    Select,
    List,
    Image,
    Tag,
    Form,
    Avatar,
    Drawer,
    Button,
    Modal,
    message, Upload, Spin,
} from "antd";
import {
    HeartOutlined,
    EyeOutlined,
    ArrowUpOutlined,
    StarOutlined,
    StarFilled,
    SearchOutlined,
    ArrowDownOutlined,
    UserOutlined, LoadingOutlined, PlusOutlined, UploadOutlined
} from "@ant-design/icons";
import axios from "axios";
import {NavLink, useNavigate, useLocation} from "react-router-dom";

const baseurl = "https://6cbpmuhemh.execute-api.us-east-2.amazonaws.com/dev/";
const uploadurl = "https://xpu7xvvdcg.execute-api.us-east-2.amazonaws.com/dev/user-avatars-bucket/"

const Home = () => {
    const [messageApi, contextHolder] = message.useMessage(); // 页面上方提示话框
    const {Header, Footer, Sider, Content} = Layout;
    const {Search} = Input;
    const {Title} = Typography;
    const [top10_region, setTop10_region] = useState("BR"); // TOP10的地区
    const [top10_table, setTop10_table] = React.useState(null); // TOP10的Table
    const [top10_category, setTop10_category] = useState(0); // TOP10的Category
    const [category, setCategory] = useState(null);
    const [tile_or_channel, setTitle_or_channel] = useState('Title');
    const [weekly_best_table, setWeekly_best_table] = React.useState(null);
    const [video, setVideo] = React.useState(null);
    const [search_value, setSearch_value] = useState("");
    const [week_weekly, setWeek_weekly] = useState([]);
    const [region_main, setRegion_main] = useState(null);
    const [category_main, setCategory_main] = useState(null);
    const [channel_main, setChannel_main] = useState(null);
    const [sort_main, setSort_main] = useState("PublishedAt");
    const [category_blank, setCategory_blank] = useState([]);
    const [current_channel, setCurrent_channel] = useState('Channel');
    const [userPassword, setUserPassword] = useState(null);
    const [userName, setUserName] = useState('UnLogin');
    const [userGender, setUserGender] = useState(null);
    const [userAvatar, setUserAvatar] = useState(null);
    const [userId, setUserId] = useState(null);
    const [drawerOpen, setDrawerOpen] = useState(0);
    const location = useLocation();
    const userInfo = location.state || {};
    const [favoriteList, setFavoriteList] = useState(null);
    const [modal_status, setModal_status] = useState(0);
    const [upload_file_type, setUpload_file_type] = useState(null);
    const [form_modal] = Form.useForm();
    const [upload_loading, setUpload_loading] = useState(false)
    const [login_status, setLogin_status] = useState(0);
    const [week, setWeek] = useState(null);
    const [week_list, setWeek_list] = useState(null);

    const Top_10 = [
        {
            title: "TOP 10",
            dataIndex: "Title",
            key: "top",
        },
        {
            title: "Views",
            dataIndex: "ViewCount",
            key: "views",
        },
        {
            title: "Likes",
            dataIndex: "Likes",
            key: "likes",
        },
    ]
    const weekly_best = [
        {
            title: "Weekly Best",
            dataIndex: "Title",
            key: "weekly_best",
        },
        {
            title: "Views",
            dataIndex: "ViewCount",
            key: "views",
        },
        {
            title: "Likes",
            dataIndex: "Likes",
            key: "likes",
        },
    ]
    const headerStyle = {
        textAlign: 'center',
        color: '#fff',
        height: 100,
        paddingInline: 50,
        lineHeight: '64px',
        backgroundColor: '#9DCD84',
    };
    const contentStyle = {
        textAlign: 'center',
        minHeight: '100vh',
        lineHeight: '120px',
        color: '#fff',
        backgroundColor: '#9DCD84',
    };
    const siderStyle = {
        textAlign: 'center',
        lineHeight: '120px',
        minHeight: '100vh',
        color: '#fff',
        backgroundColor: '#E5FCD2',
    };

    const changeRegion = (value) => {
        setTop10_region(value);
    }

    const changeCategory = (value) => {
        setTop10_category(value);
    }

    const changeTitle_or_channel = (e) => {
        setTitle_or_channel(e.target.value);
    }

    const modalOK = async () => {
        if (upload_file_type) {
            await axios.put(`${baseurl}changeUserInfo`, {
                "UserId": userId,
                "Password": form_modal.getFieldValue("userPassword"),
                "UserName": form_modal.getFieldValue("userName"),
                "Gender": form_modal.getFieldValue("userGender"),
                "Avatar": `https://user-avatars-bucket.s3.us-east-2.amazonaws.com/${userId}${upload_file_type}`
            }, {
                headers: {
                    "x-api-key": "urLOROFoXZC3weFVmAmV7l5QtbEMOi67kBBr9UI8"
                }
            }).then(() => {
                axios.get(`${baseurl}getUserInfo?UserName=${(form_modal.getFieldValue("userName")) ? (form_modal.getFieldValue("userName")) : (userName)}`, {
                    headers: {
                        "x-api-key": "urLOROFoXZC3weFVmAmV7l5QtbEMOi67kBBr9UI8"
                    }
                }).then((response) => {
                    setUserName(response.data['data'][0]['UserName']);
                    setUserGender(response.data['data'][0]['Gender']);
                    setUserAvatar(response.data['data'][0]['Avatar']);
                    setUserPassword(response.data['data'][0]['Password']);
                    messageApi.info("Change Successfully");
                    form_modal.resetFields();
                    setModal_status(0);
                });
            }).catch(error => {
                if (form_modal.getFieldValue("userPassword").length < 8) {
                    messageApi.info("Password should have at least 8 letters.");
                } else {
                    messageApi.info("This Name has been used. Please change another one.");
                }
            });
        } else {
            await axios.put(`${baseurl}changeUserInfo`, {
                "UserId": userId,
                "Password": form_modal.getFieldValue("userPassword"),
                "UserName": form_modal.getFieldValue("userName"),
                "Gender": form_modal.getFieldValue("userGender"),
            }, {
                headers: {
                    "x-api-key": "urLOROFoXZC3weFVmAmV7l5QtbEMOi67kBBr9UI8"
                }
            }).then(() => {
                axios.get(`${baseurl}getUserInfo?UserName=${(form_modal.getFieldValue("userName")) ? (form_modal.getFieldValue("userName")) : (userName)}`, {
                    headers: {
                        "x-api-key": "urLOROFoXZC3weFVmAmV7l5QtbEMOi67kBBr9UI8"
                    }
                }).then((response) => {
                    setUserName(response.data['data'][0]['UserName']);
                    setUserGender(response.data['data'][0]['Gender']);
                    setUserAvatar(response.data['data'][0]['Avatar']);
                    setUserPassword(response.data['data'][0]['Password']);
                    messageApi.info("Change Successfully");
                    form_modal.resetFields();
                    setModal_status(0);
                });
            }).catch(error => {
                if (form_modal.getFieldValue("userPassword").length < 8) {
                    messageApi.info("Password should have at least 8 letters.");
                } else {
                    messageApi.info("This Name has been used. Please change another one.");
                }
            });
        }
    };

    const beforeUploadAvatar = (file) => {
        const isJpg = file.type === 'image/jpeg';
        const isPng = file.type === 'image/png';

        if (!isJpg && !isPng) {
            message.error('You can only upload JPG/PNG file!');
        }
        const isLt2M = file.size / 1024 / 1024 < 2;
        if (!isLt2M) {
            message.error('Image must smaller than 2MB!');
        }

        setUpload_file_type(isJpg ? ".jpg" : ".png");

        return (isJpg || isPng) && isLt2M;
    }

    const getBase64 = (img, callback) => {
        const reader = new FileReader();
        reader.addEventListener('load', () => callback(reader.result));
        reader.readAsDataURL(img);
    };

    const handleChangeAvatar = (info) => {
        if (info.file.status === 'uploading') {
            setUpload_loading(true);
            return;
        }
        if (info.file.status === 'done') {
            getBase64(info.file.originFileObj, (url) => {
                setUpload_loading(false);
                setUserAvatar(url);
            });
        }
    };

    let navigate = useNavigate();

    React.useEffect(() => {
        axios.get(`${baseurl}getCategory`, {
            headers: {
                "x-api-key": "urLOROFoXZC3weFVmAmV7l5QtbEMOi67kBBr9UI8"
            }
        }).then((response) => {
            setCategory(response.data['data']);
        });
        axios.get(`${baseurl}getCategory`, {
            headers: {
                "x-api-key": "urLOROFoXZC3weFVmAmV7l5QtbEMOi67kBBr9UI8"
            }
        }).then((response) => {
            const category_temp = response.data['data'];
            category_temp.push({value: 100, label: 'Category'});
            setCategory_blank(category_temp);
        });
    }, []);

    React.useEffect(() => {
        axios.get(`${baseurl}getWeeks?`, {
            headers: {
                "x-api-key": "urLOROFoXZC3weFVmAmV7l5QtbEMOi67kBBr9UI8"
            }
        }).then((response) => {
            setWeek_list(response.data['data']);
            setWeek(response.data['data'][0]['value']);
            axios.get(`${baseurl}getWeeklyBest?Week=${response.data['data'][0]['value']}`, {
                headers: {
                    "x-api-key": "urLOROFoXZC3weFVmAmV7l5QtbEMOi67kBBr9UI8"
                }
            }).then((response) => {
                setWeekly_best_table(response.data['data']);
            });
        });
    }, []);

    React.useMemo(() => {
        if (week) {
            axios.get(`${baseurl}getWeeklyBest?Week=${week}`, {
                headers: {
                    "x-api-key": "urLOROFoXZC3weFVmAmV7l5QtbEMOi67kBBr9UI8"
                }
            }).then((response) => {
                setWeekly_best_table(response.data['data']);
            });
        }
    }, [week]);

    React.useEffect(() => {
        if (userInfo.data && login_status === 0) {
            messageApi.info("Login Successfully");
            setUserName(userInfo.data);
            axios.get(`${baseurl}getUserInfo?UserName=${userInfo.data}`, {
                headers: {
                    "x-api-key": "urLOROFoXZC3weFVmAmV7l5QtbEMOi67kBBr9UI8"
                }
            }).then((response) => {
                setUserId(response.data['data'][0]['UserId']);
                setUserGender(response.data['data'][0]['Gender']);
                setUserAvatar(response.data['data'][0]['Avatar']);
                setUserPassword(response.data['data'][0]['Password']);
                axios.get(`${baseurl}getFavorite?UserId=${response.data['data'][0]['UserId']}`, {
                    headers: {
                        "x-api-key": "urLOROFoXZC3weFVmAmV7l5QtbEMOi67kBBr9UI8"
                    }
                }).then((response) => {
                    setFavoriteList(response.data['data']);
                });
            });
            setLogin_status(1);
        }
        if (userId && login_status === 1) {
            axios.get(`${baseurl}getFavorite?UserId=${userId}`, {
                headers: {
                    "x-api-key": "urLOROFoXZC3weFVmAmV7l5QtbEMOi67kBBr9UI8"
                }
            }).then((response) => {
                setFavoriteList(response.data['data']);
            });
        }
    }, [favoriteList]);

    const [loading, setLoading] = useState(null)

    React.useMemo(() => {
        if (!search_value) {
            if (sort_main === 'Relevance') {
                setSort_main('PublishedAt');
            }
            setLoading(true)
            axios.get(`${baseurl}sortTrending?SortBy=${sort_main || ""}&Region=${region_main || ""}&CategoryId=${category_main || ""}&ChannelId=${channel_main || ""}`, {
                headers: {
                    "x-api-key": "urLOROFoXZC3weFVmAmV7l5QtbEMOi67kBBr9UI8"
                }
            }).then((response) => {
                setWeek_weekly(response.data['data']);
                setLoading(false)
            });
        } else {
            setLoading(true)
            axios.get(`${baseurl}searchVideo?Prompt=${search_value}&SortBy=${sort_main || ""}&Region=${region_main || ""}&CategoryId=${category_main || ""}&ChannelId=${channel_main || ""}`, {
                headers: {
                    "x-api-key": "urLOROFoXZC3weFVmAmV7l5QtbEMOi67kBBr9UI8"
                }
            }).then((response) => {
                setWeek_weekly(response.data['data']);
                setLoading(false)
            });
        }
    }, [search_value, channel_main, category_main, sort_main, region_main]);

    React.useMemo(() => {
        axios.get(`${baseurl}topTen?SelectedColumn=${tile_or_channel}&CategoryId=${top10_category}&Region=${top10_region}&SortBy=likes`, {
            headers: {
                "x-api-key": "urLOROFoXZC3weFVmAmV7l5QtbEMOi67kBBr9UI8"
            }
        }).then((response) => {
            setTop10_table(response.data['data']);
        });
    }, [top10_region, top10_category, tile_or_channel]);

    return (
        <>
            {contextHolder}
            <Drawer placement="right" onClose={() => {
                setDrawerOpen(0);
            }} open={drawerOpen}>
                {(userId === null) ? (
                    <>
                        <Title level={4} style={{margin: '18px', fontFamily: 'Orbitron'}}> Please Login First </Title>
                        <Space direction='horizontal'>
                            <Button type="primary" style={{margin: '15px', width: '100px', fontFamily: 'Orbitron'}}
                                    onClick={() => {
                                        navigate('/LogIn');
                                    }}>
                                LogIn
                            </Button>
                            <Button type="primary" style={{margin: '1px', width: '100px', fontFamily: 'Orbitron'}}
                                    onClick={() => {
                                        navigate('/Register');
                                    }}>
                                Register
                            </Button>
                        </Space>
                    </>
                ) : (
                    <Space direction='vertical' size={1}>
                        <Title level={4} style={{margin: '18px', fontFamily: 'Orbitron'}}> UserInformation </Title>
                        <div style={{margin: '20px', fontFamily: 'Orbitron'}}>
                            User Name: {userName}
                        </div>
                        <div style={{margin: '20px', fontFamily: 'Orbitron'}}>
                            User Gender: {(userGender) ? (userGender) : ("Undefined")}
                        </div>
                        <div style={{margin: '20px', fontFamily: 'Orbitron'}}>
                            User Favorite:
                        </div>
                        {(favoriteList === null) ? null : (
                            <List
                                itemLayout="vertical"
                                size="large"
                                pagination={{
                                    pageSize: 10,
                                    hideOnSinglePage: true,
                                }}
                                dataSource={favoriteList}
                                renderItem={(item) => (
                                    <List.Item key={item.VideoId} style={{textAlign: 'left'}}>
                                        <Space direction='horizontal'>
                                            <div>
                                                {item.Title}
                                            </div>
                                            <div style={{fontFamily: 'Orbitron', color: 'red'}} onClick={() => {
                                                axios.delete(`${baseurl}favoriteDelete?VideoId=${item.VideoId}&UserId=${userId}`, {
                                                    data: {
                                                        "VideoId": item.VideoId,
                                                        "UserId": userId
                                                    },
                                                    headers: {
                                                        "x-api-key": "urLOROFoXZC3weFVmAmV7l5QtbEMOi67kBBr9UI8"
                                                    }
                                                }).then(
                                                    axios.get(`${baseurl}getFavorite?UserId=${userId}`, {
                                                        headers: {
                                                            "x-api-key": "urLOROFoXZC3weFVmAmV7l5QtbEMOi67kBBr9UI8"
                                                        }
                                                    }).then((response) => {
                                                        setFavoriteList(response.data['data']);
                                                    })
                                                ).catch((error) => {
                                                })
                                            }}>
                                                delete
                                            </div>
                                        </Space>
                                    </List.Item>
                                )}
                            />
                        )}
                        <Button type="primary" style={{margin: '20px', fontFamily: 'Orbitron'}} onClick={() => {
                            setModal_status(1)
                        }}>
                            Change User's Information
                        </Button>
                        <Button type="primary" style={{margin: '20px', fontFamily: 'Orbitron'}} onClick={() => {
                            setUserId(null);
                            setUserAvatar(null);
                            setUserGender(null);
                            setUserGender(null);
                            setUserPassword(null);
                            setUserName(null);
                        }}>
                            Log out
                        </Button>
                    </Space>
                )}
            </Drawer>
            <Modal title="Change Information" style={{fontFamily: 'Orbitron'}} open={modal_status} onOk={modalOK}
                   onCancel={() => {
                       setModal_status(0);
                       form_modal.resetFields();
                   }}>
                <Form form={form_modal}>
                    <ImgCrop rotationSlider>
                        <Upload
                            name="avatar"
                            listType="picture-circle"
                            className="avatar-uploader"
                            showUploadList={false}
                            beforeUpload={beforeUploadAvatar}
                            onChange={handleChangeAvatar}

                            customRequest={async (options) => {
                                const {onSuccess, onError, file, onProgress} = options;

                                const config = {
                                    url: `${uploadurl}${userId}${file.type === 'image/jpeg' ? ".jpg" : ".png"}`,
                                    headers: {
                                        "x-api-key": "urLOROFoXZC3weFVmAmV7l5QtbEMOi67kBBr9UI8",
                                    },
                                    method: "PUT",
                                    data: file
                                }

                                axios.request(config).then(() => onSuccess("Ok")).catch((error) => onError(error))
                            }}
                        >
                            {userAvatar ? (
                                <img
                                    src={userAvatar}
                                    alt="avatar"
                                    style={{
                                        width: '100%',
                                    }}
                                />
                            ) : (
                                <div>
                                    {upload_loading ? <LoadingOutlined/> : <PlusOutlined/>}
                                    <div
                                        style={{
                                            marginTop: 8,
                                        }}
                                    >
                                        Upload
                                    </div>
                                </div>
                            )}
                        </Upload>
                    </ImgCrop>
                    <Form.Item
                        label={<span style={{fontFamily: 'Orbitron'}}>
                            userName:
                        </span>}
                        name="userName"
                        style={{width: '400px', marginTop: '20px', fontFamily: 'Orbitron'}}
                    >
                        <Input placeholder={userName}/>
                    </Form.Item>
                    <Form.Item
                        label={<span style={{fontFamily: 'Orbitron'}}>
                            Gender:
                        </span>}
                        name="userGender"
                        style={{width: '400px', marginTop: '20px', fontFamily: 'Orbitron'}}
                    >
                        <Input placeholder={userGender}/>
                    </Form.Item>
                    <Form.Item
                        label={<span style={{fontFamily: 'Orbitron'}}>
                            Password:
                        </span>}
                        name="userPassword"
                        style={{width: '400px', marginTop: '20px', fontFamily: 'Orbitron'}}
                    >
                        <Input.Password placeholder="*********"/>
                    </Form.Item>
                </Form>
            </Modal>
            <Layout>
                <Sider style={siderStyle} width={460}>
                    <Space direction="vertical" size={10} style={{display: 'flex'}}>
                        <Search placeholder="Search Your Video" style={{width: '300px', marginTop: '50px'}}
                                onSearch={(value) => {
                                    setSearch_value(value);
                                }}/>
                        <Card style={{margin: '12px'}}>
                            <Title level={4} style={{
                                marginTop: '5px',
                                fontFamily: 'Dancing Script',
                                display: 'flex',
                                margin: '12px'
                            }}>
                                TOP 10 Videos
                            </Title>
                            <Space direction="horizontal" size={12} style={{display: 'flex'}}>
                                <Select
                                    defaultValue="BR"
                                    style={{
                                        width: 97,
                                        marginTop: '5px'
                                    }}
                                    onChange={changeRegion}
                                    options={[
                                        {
                                            value: 'BR',
                                            label: 'BR',
                                        },
                                        {
                                            value: 'CA',
                                            label: 'CA',
                                        },
                                        {
                                            value: 'DE',
                                            label: 'DE',
                                        },
                                        {
                                            value: 'FR',
                                            label: 'FR',
                                        },
                                        {
                                            value: 'GB',
                                            label: 'GB',
                                        },
                                        {
                                            value: 'IN',
                                            label: 'IN',
                                        },
                                        {
                                            value: 'JP',
                                            label: 'JP',
                                        }, {
                                            value: 'KR',
                                            label: 'KR',
                                        },
                                        {
                                            value: 'MX',
                                            label: 'MX',
                                        },
                                        {
                                            value: 'RU',
                                            label: 'RU',
                                        },
                                        {
                                            value: 'US',
                                            label: 'US',
                                        },
                                    ]}
                                />
                                <Select
                                    defaultValue="Film & Animation"
                                    style={{
                                        width: 97,
                                        marginTop: '5px'
                                    }}
                                    onChange={changeCategory}
                                    options={category}
                                />
                                <Radio.Group value={tile_or_channel} onChange={changeTitle_or_channel} style={{
                                    width: 170,
                                    marginTop: '5px'
                                }}>
                                    <Radio.Button value="Title">Title</Radio.Button>
                                    <Radio.Button value="ChannelTitle">ChannelTitle</Radio.Button>
                                </Radio.Group>
                            </Space>
                            <Table
                                style={{
                                    marginTop: '5px'
                                }}
                                columns={Top_10}
                                dataSource={top10_table}
                                rowKey="Title"
                                pagination={{hideOnSinglePage: true}}
                            />
                        </Card>
                        <Card style={{margin: '12px'}}>
                            <Space direction='horizontals'>
                                <Title level={4} style={{
                                    marginTop: '5px',
                                    fontFamily: 'Dancing Script',
                                    display: 'flex',
                                    margin: '12px'
                                }}>
                                    Weekly Best Watch
                                </Title>
                                <div style={{width: '65px'}}>

                                </div>
                                <Select
                                    defaultValue={"Last Week"}
                                    style={{
                                        width: 130,
                                        marginTop: '10px'
                                    }}
                                    onChange={(value) => {
                                        setWeek(value);
                                    }}
                                    options={week_list}
                                />
                            </Space>
                            <Table
                                style={{
                                    marginTop: '5px'
                                }}
                                columns={weekly_best}
                                dataSource={weekly_best_table}
                                rowKey="Title"
                                pagination={{hideOnSinglePage: true}}
                            />
                        </Card>
                    </Space>
                </Sider>
                <Layout>
                    <Header style={headerStyle}>
                        <Space direction="horizontal">
                            <div style={{width: '270px'}}/>
                            <Title style={{color: 'white', fontFamily: 'Dancing Script'}}>
                                Youtube Best Collection
                            </Title>
                            <div style={{width: '230px'}}/>
                            {(userAvatar) ? (
                                <Avatar src={userAvatar} size={50} icon={<UserOutlined/>} onClick={() => {
                                    setDrawerOpen(1);
                                }}/>
                            ) : (
                                <Avatar size={50} icon={<UserOutlined/>} onClick={() => {
                                    setDrawerOpen(1);
                                }}/>
                            )}
                            <div style={{margin: '10px', color: 'black', fontFamily: 'Orbitron'}}> {userName} </div>
                        </Space>
                        <Space direction="horizontal" size={15} style={{display: 'flex'}}>
                            {(channel_main === null) ? (
                                <Tag bordered={false} color="geekblue" style={{width: "200px", textAlign: 'center'}}>
                                    Channel
                                </Tag>
                            ) : (
                                <Tag bordered={false} color="geekblue" style={{width: "200px", textAlign: 'center'}}
                                     onClick={() => {
                                         setChannel_main(null);
                                     }}>
                                    {current_channel}
                                </Tag>
                            )
                            }
                            {(category_main === null) ? (
                                <Select
                                    defaultValue="Category"
                                    style={{
                                        width: 150,
                                        marginTop: '5px'
                                    }}
                                    onChange={(value) => {
                                        if (value === 100) {
                                            setCategory_main(null);
                                        } else {
                                            setCategory_main(value);
                                        }
                                    }}
                                    options={category_blank}
                                />
                            ) : (
                                <Tag bordered={false} color="cyan" onClick={() => {
                                    setCategory_main(null);
                                }} style={{width: "142px", textAlign: 'center'}}>
                                    {category[category_main]['label']}
                                </Tag>
                            )
                            }
                            {(search_value) ? (<div style={{width: '100px'}}/>) : ((region_main === null) ? (
                                <Select
                                    defaultValue="Region"
                                    style={{
                                        width: 100,
                                        marginTop: '10px',
                                    }}
                                    onChange={(value) => {
                                        if (value === "Region") {
                                            setRegion_main(null);
                                        } else {
                                            setRegion_main(value);
                                        }
                                    }}
                                    options={[
                                        {
                                            value: 'Region',
                                            label: 'Region',
                                        },
                                        {
                                            value: 'BR',
                                            label: 'BR',
                                        },
                                        {
                                            value: 'CA',
                                            label: 'CA',
                                        },
                                        {
                                            value: 'DE',
                                            label: 'DE',
                                        },
                                        {
                                            value: 'FR',
                                            label: 'FR',
                                        },
                                        {
                                            value: 'GB',
                                            label: 'GB',
                                        },
                                        {
                                            value: 'IN',
                                            label: 'IN',
                                        },
                                        {
                                            value: 'JP',
                                            label: 'JP',
                                        }, {
                                            value: 'KR',
                                            label: 'KR',
                                        },
                                        {
                                            value: 'MX',
                                            label: 'MX',
                                        },
                                        {
                                            value: 'RU',
                                            label: 'RU',
                                        },
                                        {
                                            value: 'US',
                                            label: 'US',
                                        },
                                    ]}
                                />
                            ) : (
                                <Tag bordered={false} color="orange" onClick={() => {
                                    setRegion_main(null);
                                }} style={{width: "92px", textAlign: 'center'}}>
                                    {region_main}
                                </Tag>
                            ))
                            }
                            <div style={{width: '380px'}}/>
                            {(search_value) ? (
                                <Select
                                    defaultValue="Relevance"
                                    style={{
                                        width: 160,
                                        marginTop: '10px',
                                    }}
                                    onChange={(value) => {
                                        setSort_main(value);
                                    }}
                                    options={[
                                        {
                                            value: 'Relevance',
                                            label: 'Relevance',
                                        },
                                        {
                                            value: 'PublishedAt',
                                            label: 'Newest',
                                        },
                                        {
                                            value: 'Likes',
                                            label: 'Most Likes',
                                        },
                                        {
                                            value: 'ViewCount',
                                            label: 'Most View Counts ',
                                        },
                                    ]}
                                />
                            ) : (
                                <Select
                                    defaultValue="PublishedAt"
                                    style={{
                                        width: 160,
                                        marginTop: '10px',
                                    }}
                                    onChange={(value) => {
                                        setSort_main(value);
                                    }}
                                    options={[
                                        {
                                            value: 'PublishedAt',
                                            label: 'Newest',
                                        },
                                        {
                                            value: 'Likes',
                                            label: 'Most Likes',
                                        },
                                        {
                                            value: 'ViewCount',
                                            label: 'Most View Counts ',
                                        },
                                    ]}
                                />
                            )}

                        </Space>
                    </Header>
                    <Content style={contentStyle}>
                        <Card style={{margin: '15px', marginTop: '43px'}}>
                            {loading ? <Spin/> :
                                <List
                                    itemLayout="vertical"
                                    size="large"
                                    pagination={{
                                        pageSize: 5,
                                    }}
                                    dataSource={week_weekly}
                                    renderItem={(item) => (
                                        <List.Item key={item.VideoId} style={{textAlign: 'left'}}>
                                            <Space direction="horizontal">
                                                <Image width={400} height={200} src={item.ThumbnailLink}/>
                                                <Space size={5} direction="vertical">
                                                    <Title level={4} style={{
                                                        margin: '12px',
                                                        width: '450px',
                                                        marginTop: '3px',
                                                        fontFamily: 'Permanent Marker'
                                                    }}>
                                                        {item.Title}
                                                    </Title>
                                                    <div style={{margin: '15px'}}> Published
                                                        Date: {item.PublishedAt}</div>
                                                    <div style={{margin: '15px'}} onClick={() => {
                                                        window.location.href = `https://www.youtube.com/watch?v=${item.VideoId}`;
                                                    }}> VideoID : {item.VideoId}</div>
                                                    <Space direction="horizontal">
                                                        <Tag bordered={false} color="geekblue"
                                                             style={{margin: '12px', fontFamily: 'Arial'}}
                                                             onClick={() => {
                                                                 setChannel_main(item.ChannelId);
                                                                 setCurrent_channel(item.ChannelTitle);
                                                             }}>
                                                            {item.ChannelTitle}
                                                        </Tag>
                                                        <Tag bordered={false} color="cyan" onClick={() => {
                                                            setCategory_main(item.CategoryId);
                                                        }}>
                                                            {item.CategoryTitle}
                                                        </Tag>
                                                        <Tag bordered={false} color="orange" onClick={() => {
                                                            setRegion_main(item.Region);
                                                        }}>
                                                            {item.Region}
                                                        </Tag>
                                                    </Space>
                                                </Space>
                                                <Space size={30} direction="vertical" style={{margin: '20px'}}>
                                                    <Space direction="horizontal" size={10}>
                                                        <HeartOutlined
                                                            style={{fontSize: '20px', color: 'red', marginTop: '5px'}}/>
                                                        <div style={{margin: '5px'}}>
                                                            {item.Likes}
                                                        </div>
                                                        {(item.LikesChange < 0) ? (
                                                            <Space direction="horizontal" size={1}>
                                                                <ArrowDownOutlined
                                                                    style={{marginTop: '5px', color: 'red'}}/>
                                                                <div style={{margin: '1px'}}>
                                                                    {item.LikesChange}
                                                                </div>
                                                            </Space>
                                                        ) : (
                                                            <Space direction="horizontal" size={1}>
                                                                <ArrowUpOutlined
                                                                    style={{marginTop: '5px', color: 'red'}}/>
                                                                <div style={{margin: '1px'}}>
                                                                    {item.LikesChange}
                                                                </div>
                                                            </Space>
                                                        )}
                                                    </Space>
                                                    <Space direction="horizontal" size={10}>
                                                        <EyeOutlined
                                                            style={{
                                                                fontSize: '20px',
                                                                color: 'orange',
                                                                marginTop: '7px'
                                                            }}/>
                                                        <div style={{margin: '5px'}}>
                                                            {item.ViewCount}
                                                        </div>
                                                        {item.ViewCountChange === 0 ? null : (
                                                            <Space direction="horizontal" size={1}>
                                                                <ArrowUpOutlined
                                                                    style={{marginTop: '5px', color: 'orange'}}/>
                                                                <div style={{margin: '1px'}}>
                                                                    {item.ViewCountChange}
                                                                </div>
                                                            </Space>
                                                        )}
                                                    </Space>
                                                    {(userId && favoriteList) ? (
                                                        <Space direction="horizontal" size={10}>
                                                            {favoriteList.map(item => item.VideoId).includes(item.VideoId) === false ? (
                                                                <>
                                                                    <StarOutlined style={{
                                                                        fontSize: '20px',
                                                                        color: 'gold',
                                                                        marginTop: '7px'
                                                                    }} onClick={() => {
                                                                        axios.post(`${baseurl}favoriteInsert`, {
                                                                            "VideoId": item.VideoId,
                                                                            "UserId": userId
                                                                        }, {
                                                                            headers: {
                                                                                "x-api-key": "urLOROFoXZC3weFVmAmV7l5QtbEMOi67kBBr9UI8"
                                                                            }
                                                                        }).then(
                                                                            axios.get(`${baseurl}getFavorite?UserId=${userId}`, {
                                                                                headers: {
                                                                                    "x-api-key": "urLOROFoXZC3weFVmAmV7l5QtbEMOi67kBBr9UI8"
                                                                                }
                                                                            }).then((response) => {
                                                                                setFavoriteList(response.data['data']);
                                                                            })
                                                                        ).catch((error) => {

                                                                            }
                                                                        )
                                                                    }}/>
                                                                    <div style={{margin: '5px'}}>
                                                                        Add to your Favorite
                                                                    </div>
                                                                </>
                                                            ) : (
                                                                <>
                                                                    <StarFilled style={{
                                                                        fontSize: '20px',
                                                                        color: 'gold',
                                                                        marginTop: '7px'
                                                                    }} onClick={() => {
                                                                        axios.delete(`${baseurl}favoriteDelete?VideoId=${item.VideoId}&UserId=${userId}`, {
                                                                            data: {
                                                                                "VideoId": item.VideoId,
                                                                                "UserId": userId
                                                                            },
                                                                            headers: {
                                                                                "x-api-key": "urLOROFoXZC3weFVmAmV7l5QtbEMOi67kBBr9UI8"
                                                                            }
                                                                        }).then(
                                                                            axios.get(`${baseurl}getFavorite?UserId=${userId}`, {
                                                                                headers: {
                                                                                    "x-api-key": "urLOROFoXZC3weFVmAmV7l5QtbEMOi67kBBr9UI8"
                                                                                }
                                                                            }).then((response) => {
                                                                                setFavoriteList(response.data['data']);
                                                                            })
                                                                        ).catch((error) => {
                                                                        });
                                                                    }}/>
                                                                    <div style={{margin: '5px'}}>
                                                                        Cancel
                                                                    </div>
                                                                </>
                                                            )}
                                                        </Space>
                                                    ) : null}
                                                </Space>
                                            </Space>
                                        </List.Item>
                                    )}
                                />
                            }
                        </Card>
                    </Content>
                </Layout>
            </Layout>
        </>
    );
}

export default Home;
