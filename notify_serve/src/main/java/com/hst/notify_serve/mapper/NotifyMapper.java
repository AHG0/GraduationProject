package com.hst.notify_serve.mapper;

import com.alibaba.fastjson.JSONObject;
import com.hst.notify_serve.entity.Notify;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface NotifyMapper extends BaseMapper<Notify> {
    @Select("select * from notify")
    List<JSONObject> select();
}
