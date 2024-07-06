package com.hst.file_serve.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.hst.user_serve.entity.User;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Update;

@Mapper
public interface UserInfoMapper extends BaseMapper<User> {
    @Update("update user set queries_num=queries_num-#{file_num} where userid=#{userid}")
    void decUserQueriesNum(int userid, int file_num);
}
