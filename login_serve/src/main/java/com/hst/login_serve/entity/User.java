package com.hst.login_serve.entity;


import com.baomidou.mybatisplus.annotation.TableId;
import lombok.Data;
import org.springframework.stereotype.Component;

@Data
@Component
public class User {
    @TableId("userid")
    private Integer userid;
    private String username;
    private String password;
    private boolean permission;
    private String phone;
    private String mail;
    //用户会员等级（普通：0，中级：1，高级：2）
    private Integer usertype;
    //过期时间
    private String expire_date;
    //每天剩余可查询次数
    private Integer queries_num;
    //token
    private String token;
    //注册日期
    private String registration_day;

    public boolean getPermission() {
        return this.permission;
    }
}
