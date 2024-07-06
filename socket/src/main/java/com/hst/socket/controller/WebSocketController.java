package com.hst.socket.controller;

import com.hst.socket.service.WebSocketService;
import com.hst.user_serve.service.impl.UserServiceImpl;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.ModelAndView;

import java.io.IOException;


@RestController
public class WebSocketController {
    UserServiceImpl userServiceImpl = new UserServiceImpl();
    @GetMapping("/page")
    public ModelAndView page() {
        return new ModelAndView("webSocket");
    }

    @RequestMapping("/push/{toUID}")
    public ResponseEntity<String> pushToClient(String message, @PathVariable String toUID) throws IOException {
        WebSocketService.sendInfo(message, toUID);
        return ResponseEntity.ok("Send Success!");
    }

    @RequestMapping("/update_queries_num")
    public void update_queries_num(@RequestParam("userid") int userid, @RequestParam("queries_num") int queries_num) {
        userServiceImpl.updateQueriesNum(userid, queries_num);
        System.out.println("————————————更新成功————————————");
    }
}