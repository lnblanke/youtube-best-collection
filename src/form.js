import React from 'react';
import { Form, Input , Modal, DatePicker} from 'antd';
import PropTypes from 'prop-types'


function formConsist(props) {
     
    return (
        <Modal title="Input / Change your information" open={props.isModalOpen} onOk={props.handleOk} onCancel={props.handleCancel}>

            <Form form={props.form}>
                {
                props.put_or_post ? null : 
                <Form.Item
                    label="Badge"
                    name="badge"
                    rules={[
                        {
                          required: true,
                          message: 'Please input your badge',
                        },
                    ]}
                >
                    <Input />
                </Form.Item>
              }
              <Form.Item
                label="Name"
                name="name"
                rules={[
                  {
                    required: true,
                    message: 'Please input your name',
                  },
                ]}
              >
                <Input />
              </Form.Item>

              <Form.Item
                label="Name_en"
                name="name_en"
                rules={[
                  {
                    required: true,
                    message: 'Please input your name in English',
                  },
                ]}
              >
                <Input />
              </Form.Item>


              <Form.Item
                label="Email"
                name="email"
                rules={[
                  {
                    required: true,
                    message: 'Please input your email',
                  },
                ]}
              >
                <Input />
              </Form.Item>

              <Form.Item
                label="Jointime"
                name="jointime"
                rules={[
                  {
                    required: true,
                    message: 'Please input your Jointime',
                  },
                ]}
              >
                <DatePicker Item = "YYYY-MM-DD"/>
              </Form.Item>

              <Form.Item
                label="Bu"
                name="bu"
                rules={[
                  {
                    required: true,
                    message: 'Please input your BU',
                  },
                ]}
              >
                <Input />
              </Form.Item>

              <Form.Item
                label="Dept"
                name="dept"
                rules={[
                  {
                    required: true,
                    message: 'Please input your Dept',
                  },
                ]}
              >
                <Input />
              </Form.Item>
            </Form> 
        </Modal>
    );
};

formConsist.propTypes = {
    put_or_post: PropTypes.bool,
    form: PropTypes.object,
    isModalOpen: PropTypes.bool,
    handleOk: PropTypes.func,
    handleCancel: PropTypes.func
}

export default formConsist