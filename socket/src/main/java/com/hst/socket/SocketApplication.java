package com.hst.socket;

import com.baomidou.mybatisplus.autoconfigure.DdlApplicationRunner;
import com.hst.socket.service.SQLThread;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.context.annotation.Bean;

import java.util.List;

@SpringBootApplication
public class SocketApplication {

	public static void main(String[] args) {
		ConfigurableApplicationContext context = SpringApplication.run(SocketApplication.class, args);
		SQLThread.setApplicationContext(context);
		//SpringApplication.run(SocketApplication.class, args);
	}

	@Bean
	public DdlApplicationRunner ddlApplicationRunner(@Autowired(required = false) List ddlList) {
		return new DdlApplicationRunner(ddlList);
	}
}
