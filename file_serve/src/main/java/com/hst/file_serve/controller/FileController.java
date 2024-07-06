package com.hst.file_serve.controller;

import com.alibaba.fastjson.JSONArray;
import com.hst.file_serve.service.FileEntityService;
import com.alibaba.fastjson.JSONObject;
import com.hst.file_serve.service.impl.FileEntityServiceImpl;
import com.hst.file_serve.utils.FileEntityUtils;
import com.hst.user_serve.jwt.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

//接收多个文件
@CrossOrigin
@RestController
public class FileController {
    List<JSONObject> entityResults = new ArrayList<>();
    @Autowired
    FileEntityService fileEntityService;
    @Autowired
    FileEntityServiceImpl fesi;
    JwtUtil jwtUtil = new JwtUtil();
    private int userid;
    private int[] fileNum = new int[]{1, 2, 100};
    private int[] preFileNum = new int[]{1, 2, 1000};

    //测试webSocket
    @RequestMapping("/webSocket/2")
    public int uploadFile() {
        return 1;
    }

    @RequestMapping("/uploadFile")
    public int uploadFile(@RequestHeader("token") String token, @RequestParam("usertype") int usertype, @RequestParam("files") MultipartFile[] files) {
        JSONObject tokenData = jwtUtil.verifyToken(token);
        int userid = tokenData.getInteger("userid");
        if (tokenData.getBoolean("verify")) {
            List<String> ContentList = new ArrayList<>();//保存文件内容
            List<String> NameList = new ArrayList<>();//保存文件名称
            try {
                for (MultipartFile file : files) {
                    // 打印文件名
                    String fileName = file.getOriginalFilename();
                    // 读取文件内容并打印
                    String fileContent = new String(file.getBytes());
                    String fileContentReplace = fileContent.replaceAll("\\s+", ", ");
                    String[] splitStrings = fileContentReplace.split(", ");
                    for (String i : splitStrings) {
                        ContentList.add(i);
                        NameList.add(fileName);
                    }
                }
                System.out.println(ContentList);
                System.out.println(NameList);
                //检测文件提交数量
                if (NameList.size() > fileNum[usertype]) {
                    //提交文件数量过多
                    return 3;
                }
                for (String content : ContentList) {
                    if (content.length() > preFileNum[usertype]) {
                        //单个文件文字数量过多
                        return 4;
                    }
                }
                FileEntityUtils eu = new FileEntityUtils();

                entityResults = eu.UseEntityThread(ContentList);
                if (Objects.equals(entityResults.toString(), "[{}]")) {
                    return 5;
                }
                System.out.println(entityResults);

                System.out.println("-----执行中-----");
                for (int i = 0; i < entityResults.size(); i++) {
                    fileEntityService.insertEntity(entityResults.get(i), ContentList.get(i), NameList.get(i), userid);
                }
                System.out.println("----执行完毕----");
                //nameList去重
                List<String> newList = new ArrayList<>();
                NameList.forEach(str -> {
                    if (!newList.contains(str)) {
                        newList.add(str);
                    }
                });
                //提交次数count+=file_num，提交次数为文件数量
                fileEntityService.subCountAdd(userid, newList.size(), fileEntityService.getDay());
                //用户可查询次数-文件数量
                fileEntityService.decUserQueriesNum(userid, newList.size());
                //上传成功
                return 0;
            } catch (IOException e) {
                e.printStackTrace();
                //上传失败
                return 1;
            }
        } else {
            //token解析失败
            return 2;
        }
    }

    @GetMapping("/submitUserId")
    public void getUserId(@RequestHeader("token") String token) {
        JSONObject tokenData = jwtUtil.verifyToken(token);
        this.userid = tokenData.getInteger("userid");
        System.out.println(this.userid);
    }

    @GetMapping("/selectFEntity")
    public JSONArray selectEntity() {
        return fileEntityService.selectE();
    }

    @GetMapping("/selectFEntityByUserId")
    public List<JSONObject> selectFEntityByUserId(@RequestParam("userid") int userid) {
        return fileEntityService.selectByUserId(userid);
    }

    @GetMapping("/selectFEName")
    public JSONArray selectFEName() {
        return fileEntityService.selectEName();
    }

    @GetMapping("/selectFEntityData")
    public List<JSONObject> selectEntityData(@RequestHeader("token") String token, @RequestParam("name") String name) {
        return fileEntityService.selectEData(name, jwtUtil.verifyToken(token).getInteger("userid"));
    }

    @GetMapping(value = "/deleteFEName")
    public boolean deleteEntity(@RequestParam("name") String name) {
        return fileEntityService.deleteEntity(name);
    }

    @RequestMapping("/selectFERecordByUserId")
    public List<JSONObject> selectFERecordByUserId(@RequestParam("userid") int userid) {
        return fileEntityService.selectRecordByUserId(userid);
    }
}

//接收单个文件
//public class FileController {
//    @RequestMapping(value = "/uploadFile")
//    public String getFile(@RequestParam("file") MultipartFile file) {
//        try {
//            // 打印文件名
//            System.out.println("Received file: " + file.getOriginalFilename());
//
//            // 读取文件内容并打印
//            String content = new String(file.getBytes());
//            System.out.println("File content: " + content);
//
//            // 返回成功提示
//            return "File upload success!";
//        } catch (IOException e) {
//            e.printStackTrace();
//            // 返回失败提示
//            return "File upload failed!";
//        }
//    }
//}
