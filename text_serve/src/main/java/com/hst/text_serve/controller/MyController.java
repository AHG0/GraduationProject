package com.hst.text_serve.controller;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.hst.text_serve.service.MyService;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.Map;


@RestController
public class MyController {
    @Autowired
    private MyService myService;

    @GetMapping(value = "/Classify")
    public JSONObject getClassify(@RequestParam("input") String input) {
        JSONObject obj = myService.getClassify(input);
        myService.insertClassify();
        return obj;
    }

    @RequestMapping(value = "/Entity", method = RequestMethod.POST)
    public JSONObject getEntity(@RequestBody Map<String,String> param, HttpServletRequest request) {
        String input = param.get("input");
        int userid = Integer.parseInt(param.get("userid"));
        JSONObject obj = myService.getEntity(input);
        if (obj == null) {
            return obj;
        } else {
            myService.insertEntity(obj, input, userid);
        }
        return obj;
    }

    @GetMapping("/selectEntity")
    public JSONArray selectEntity() {
        return myService.selectE();
    }

    @GetMapping("/selectEntityData")
    public JSONObject selectEntityData(@RequestParam("input") String input) {
        return myService.selectEData(input);
    }

    @GetMapping("/selectClassify")
    public JSONArray selectClassify() {
        return myService.selectC();
    }

    @GetMapping("/selectClassifyData")
    public JSONObject selectClassifyData(@RequestParam("input") String input) {
        return myService.selectCData(input);
    }

    @GetMapping(value = "/deleteEntity")
    public boolean deleteEntity(@RequestParam("input") String input) {
        return myService.deleteEntity(input);
    }

    @GetMapping(value = "/deleteClassify")
    public boolean deleteClassify(@RequestParam("input") String input) {
        return myService.deleteClassify(input);
    }
}
