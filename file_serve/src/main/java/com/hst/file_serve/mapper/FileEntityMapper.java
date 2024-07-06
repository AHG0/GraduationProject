package com.hst.file_serve.mapper;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.hst.file_serve.entity.FileEntity;
import com.hst.file_serve.entity.SubmitRecord;
import org.apache.ibatis.annotations.*;
import org.springframework.stereotype.Component;

import java.util.List;

@Mapper
@Component
public interface FileEntityMapper extends BaseMapper<FileEntity> {
    @Select("select input from file_entity")
    List<String> selectEInput();

    @Select("select name from file_entity")
    List<String> selectEName();

    @Select("select MAX(id) from file_entity")
    String findMaxId();

    @Select("select * from file_entity where input=#{input}")
    JSONObject selectEByInput(@Param("input") String input);

    @Select("select * from file_entity where name=#{name} and userid=#{userid}")
    List<JSONObject> selectEByName(@Param("name") String name, @Param("userid") int userid);

    @Select("""
            SELECT *
            FROM file_entity
            where name=#{name} and userid=#{userid} and name in (select name
                           from file_entity
                           GROUP BY name
                           HAVING COUNT(*) >= 2)""")
    List<JSONObject> selectEByName_more(@Param("name") String name, @Param("userid") int userid);

    @Select("select * from file_entity where userid=#{userid}")
    List<JSONObject> selectFEntityByUserId(@Param("userid") int userid);

    @Delete("delete from file_entity where input=#{input}")
    boolean deleteEByInput(@Param("input") String input);
    @Delete("delete from file_entity where name=#{name}")
    boolean deleteEByName(@Param("name") String name);
}
