package com.hst.file_serve.mapper;

import com.alibaba.fastjson.JSONObject;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.hst.file_serve.entity.SubmitRecord;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;
import org.springframework.stereotype.Component;

import java.util.List;

@Mapper
@Component
public interface SubmitRecordMapper extends BaseMapper<SubmitRecord> {
    @Select("select * from submit_record where userid=#{userid} order by sub_time DESC")
    List<JSONObject> selectFEntityByUserId(@Param("userid") int userid);

    @Select("select max(id) from submit_record")
    String findId();

    @Update("update user_visit set submit_count=submit_count+#{file_num} " +
            "where userid=#{userid} and visit_day=#{sub_day}")
    void subCountAdd(int userid, int file_num, String sub_day);
}
