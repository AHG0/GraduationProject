import axios from "axios";

let base = '';
export const GetRequest = (url, data) => {
    return axios({
        method: 'GET',
        url: `${base}${url}`,
        params: {
            input: data
        },
        dataType: "json",
        data: JSON.stringify({input: data}),
        headers: {
            token: localStorage.getItem("token"),
            crossDomain: true,
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryNOwrfQfAncKahlbj'
        },
    })
}

export const GetRequestByUserId = (url, userid) => {
    return axios({
        method: 'GET',
        url: `${base}${url}`,
        params: {
            userid: userid
        },
        dataType: "json",
        data: JSON.stringify({userid: userid}),
        headers: {
            token: localStorage.getItem("token"),
            crossDomain: true,
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryNOwrfQfAncKahlbj'
        },
    })
}

export const PostRequest = (url, input, userid) => {
    return axios({
        method: 'POST',
        url: `${base}${url}`,
        dataType: "json",
        headers: {
            token: localStorage.getItem("token"),
        },
        data: {input: input, userid: userid}
    })
}

export const GetNameRequest = (url, data) => {
    return axios({
        method: 'GET',
        url: `${base}${url}`,
        params: {
            name: data
        },
        headers: {
            token: localStorage.getItem("token"),
            crossDomain: true,
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryNOwrfQfAncKahlbj'
        },
        dataType: "json",
        data: JSON.stringify({name: data}),
    })
}

export const PostFile = (url, form) => {
    return axios({
        method: 'POST',
        url: url,
        data: form,
        headers: {
            token: localStorage.getItem("token"),
            crossDomain: true,
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryNOwrfQfAncKahlbj'
        },
    });
}


export const GetRequests = (url, username, password) => {
    return axios({
        method: 'GET',
        url: `${url}`,
        params: {
            username: username,
            password: password,
        },
        dataType: "json",
        data: JSON.stringify({
            "username": username,
            "password": password
        }),
        changeOrigin: true, // 是否跨域
        async: false,
        headers:
            {
                token: localStorage.getItem("token"),
                crossDomain: true,
                'Content-Type':
                    'application/x-www-form-urlencoded'
            },
        contentType: 'application/json;charset=UTF-8',
    })
}
export const addUser = (url, username, password, phone, mail) => {
    return axios({
        method: 'GET',
        url: `${url}`,
        params: {
            username: username,
            password: password,
            phone: phone,
            mail: mail,
        },
        dataType: "json",
        data: JSON.stringify({
            "username": username,
            "password": password,
            "phone": phone,
            "mail": mail,
        }),
        changeOrigin: true, // 是否跨域
        async: false,
        headers:
            {
                token: localStorage.getItem("token"),
                crossDomain: true,
                'Content-Type':
                    'application/x-www-form-urlencoded'
            },
        contentType: 'application/json;charset=UTF-8',
    })
}

export const UserUpdate = (url, userid, key, value) => {
    return axios({
        method: 'GET',
        url: `${base}${url}`,
        params: {
            userid: userid,
            key: key,
            value: value,
        },
        dataType: "json",
        changeOrigin: true, // 是否跨域
        async: false,
        headers:
            {
                token: localStorage.getItem("token"),
                crossDomain: true,
                'Content-Type':
                    'application/x-www-form-urlencoded'
            },
        contentType: 'application/json;charset=UTF-8',
    })
}

export const AdminUpdate = (url, row) => {
    return axios({
        method: 'GET',
        url: `${base}${url}`,
        params: {
            userid: row.userid,
            username: row.username,
            usertype: row.usertype,
            phone: row.phone,
            mail: row.mail,
            password: row.password,
            queries_num: row.queries_num,
            permission: row.permission,
            expire_date: row.expire_date
        },
        dataType: "json",
        changeOrigin: true, // 是否跨域
        async: false,
        headers:
            {
                crossDomain: true,
                'Content-Type':
                    'application/x-www-form-urlencoded'
            },
        contentType: 'application/json;charset=UTF-8',
    })
}

export const numToText = (num) => {
    switch (num) {
        case 0:
            return '普通会员'
        case 1:
            return '中级会员'
        case 2:
            return '高级会员'
    }
}