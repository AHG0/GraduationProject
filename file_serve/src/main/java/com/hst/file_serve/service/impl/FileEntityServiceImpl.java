package com.hst.file_serve.service.impl;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.hst.file_serve.entity.FileEntity;
import com.hst.file_serve.entity.SubmitRecord;
import com.hst.file_serve.mapper.SubmitRecordMapper;
import com.hst.file_serve.mapper.UserInfoMapper;
import com.hst.file_serve.service.FileEntityService;
import com.hst.file_serve.utils.FileEntityUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.hst.file_serve.mapper.FileEntityMapper;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;


@Service
public class FileEntityServiceImpl implements FileEntityService {
    @Autowired
    FileEntityUtils fileEntityUtils;
    @Autowired
    FileEntityMapper fileEntityMapper;
    @Autowired
    SubmitRecordMapper submitRecordMapper;
    @Autowired
    UserInfoMapper userInfoMapper;

    @Override
    public JSONObject getEntity(String input) {
        return fileEntityUtils.getEntity(input);
    }
    @Override
    public JSONArray selectE() {
        return fileEntityUtils.getInput(fileEntityMapper.selectEInput());
    }

    @Override
    public JSONArray selectEName() {
        return fileEntityUtils.getName(fileEntityMapper.selectEName());
    }
    @Override
    public List<JSONObject> selectEData(String name, int userid) {
        try{
            return fileEntityMapper.selectEByName(name, userid);
        }catch (Exception e){
            return fileEntityMapper.selectEByName_more(name, userid);
        }
    }

    public List<JSONObject> selectByUserId(int userid){
        return fileEntityMapper.selectFEntityByUserId(userid);
    }

    public List<JSONObject> selectRecordByUserId(int userid){
        return submitRecordMapper.selectFEntityByUserId(userid);
    }


    @Override
    public void insertEntity(JSONObject object, String input, String name, int userid) {
        try {
            FileEntity fileEntity = new FileEntity();
            if (fileEntityMapper.findMaxId() == null) {
                fileEntity.setId(1);
            } else {
                fileEntity.setId(Integer.parseInt(fileEntityMapper.findMaxId()) + 1);
            }
            fileEntity.setRsl1(object.getString("rsl1"));
            fileEntity.setRsl2(object.getString("rsl2"));
            fileEntity.setRsl3(object.getString("rsl3"));
            fileEntity.setInput(input);
            fileEntity.setName(name);
            fileEntity.setUserid(userid);
            fileEntity.setSubTime(getTime());
            fileEntityMapper.insert(fileEntity);
            SubmitRecord submitRecord = new SubmitRecord();
            if (submitRecordMapper.findId() == null) {
                fileEntity.setId(1);
            } else {
                fileEntity.setId(Integer.parseInt(submitRecordMapper.findId()) + 1);
            }
            submitRecord.setRsl1(fileEntity.getRsl1());
            submitRecord.setRsl2(fileEntity.getRsl2());
            submitRecord.setRsl3(fileEntity.getRsl3());
            submitRecord.setInput(fileEntity.getInput());
            submitRecord.setName(fileEntity.getName());
            submitRecord.setUserid(fileEntity.getUserid());
            submitRecord.setSubTime(fileEntity.getSubTime());
            submitRecordMapper.insert(submitRecord);
        } catch(Exception e) {
            System.out.println("insertEntity出错："+ e.getMessage()); // 打印异常信息
            e.printStackTrace();
        }
    }
    @Override
    public boolean deleteEntity(String name) {
        return fileEntityMapper.deleteEByName(name);
    }

    public String getTime() {
        Date date = new Date();
        SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        return formatter.format(date);
    }

    public String getDay() {
        Date date = new Date();
        SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd");
        return formatter.format(date);
    }

    public void subCountAdd(int userid, int file_num, String sub_day) {
        submitRecordMapper.subCountAdd(userid ,file_num, sub_day);
    }
    public void decUserQueriesNum(int userid, int file_num){
        userInfoMapper.decUserQueriesNum(userid, file_num);
    }
}