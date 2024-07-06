package com.hst.feedback_serve.mapper;

import com.alibaba.fastjson.JSONObject;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.hst.feedback_serve.entity.Feedback;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.util.List;

@Mapper
public interface FeedbackMapper extends BaseMapper<Feedback> {
    @Select("select * from feedback")
    List<JSONObject> selectAll();
    @Select("select * from feedback where userid=#{userid}")
    List<JSONObject> selectByUserid(int userid);

    @Update("UPDATE feedback SET content=#{content} WHERE id=#{id}")
    void updateFeedback(String content, Long id);
}
