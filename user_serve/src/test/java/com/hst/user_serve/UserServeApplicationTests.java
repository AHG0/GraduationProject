package com.hst.user_serve;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.alibaba.fastjson.JSONPath;
import com.hst.user_serve.mapper.UserMapper;
import com.hst.user_serve.utils.RedisUtil;
import org.junit.jupiter.api.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.util.CollectionUtils;

import java.text.SimpleDateFormat;
import java.util.Calendar;

@SpringBootTest
@RunWith(SpringRunner.class)
class UserServeApplicationTests {
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;
    @Autowired
    UserMapper userMapper;
    @Autowired
    RedisUtil redisUtil;
    private JSONObject userInfo;

    @Test
    void contextLoads() {
        //JSONObject userJson = userMapper.selectById(2);
        //redisTemplate.opsForValue().set("userid"+2, userJson);
        //System.out.println("缓存设置成功");

        //this.userInfo = JSONObject.parseObject(JSON.toJSONString(redisUtil.get("userid" + 2)));
        //System.out.println(redisUtil.get("userid" + 2));
        // 修改字段值
        //JSONPath.set("userid" + 2, "queries_num", "60");
        //System.out.println(this.userInfo);
    }
}
