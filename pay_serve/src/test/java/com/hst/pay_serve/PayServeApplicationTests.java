package com.hst.pay_serve;

import com.hst.pay_serve.config.AliPayConfig;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.util.Calendar;
import java.util.Date;

@SpringBootTest
class PayServeApplicationTests {

    @Test
    void contextLoads() throws ParseException {
        AliPayConfig alipayConfig = new AliPayConfig();
        System.out.println(alipayConfig.getReturnUrl());
        System.out.println(alipayConfig.getNotifyUrl());

        Date date = new Date();
        SimpleDateFormat formatter = new SimpleDateFormat("yyyy-dd-MM HH:mm:ss");

        System.out.println(formatter.format(date));

        String dt = "2008-01-01";  // Start date
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
        Calendar c = Calendar.getInstance();
        c.setTime(sdf.parse(dt));
        c.add(Calendar.DATE, 1);  // number of days to add
        dt = sdf.format(c.getTime());  // dt is now the new date
        System.out.println(dt);

        int user_type = -1;
        String subject = "月付普通会员";
        if (subject.contains("普通会员")) {
            user_type = 0;
        } else if (subject.startsWith("中级会员")) {
            user_type = 1;
        } else {
            user_type = 2;
        }
        System.out.println(user_type);
    }
}
