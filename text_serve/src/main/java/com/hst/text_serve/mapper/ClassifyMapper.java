package com.hst.text_serve.mapper;

import com.alibaba.fastjson.JSONObject;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.hst.text_serve.entity.Classify;
import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface ClassifyMapper extends BaseMapper<Classify> {
    @Select("select input from classify")
    List<String> selectCInput();

    @Select("select MAX(id) from classify")
    int findMaxId();

    @Select("select * from classify where input=#{input}")
    JSONObject selectCByInput(@Param("input") String input);

    @Delete("delete from classify where input=#{input}")
    boolean deleteCByInput(@Param("input") String input);
}
