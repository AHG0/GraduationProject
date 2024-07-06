package com.hst.file_serve;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class FileServeApplicationTests {

    @Test
    void contextLoads() {
        String s = "[小城不大，风景如画：边境小镇室韦的蝶变之路, , 天问一号发射两周年，传回火卫一高清影像]";
        String cleanedString = s.replaceAll("[\\[\\]']", "");
        System.out.println(cleanedString);
    }

}
