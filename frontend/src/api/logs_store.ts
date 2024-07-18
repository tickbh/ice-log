import request from "@/utils/request";

const LOG_BASE_URL = "/api/v1/logs/store";

class LogsStoreAPI {
  /**
   * 获取日志分页列表
   *
   * @param queryParams 查询参数
   */
  static getPage(queryParams: LogsStorePageQuery) {
    return request<any, PageResult<LogsStorePageVO[]>>({
      url: `${LOG_BASE_URL}/page`,
      method: "get",
      params: queryParams,
    });
  }

  static update(id: number, data: LogStoreForm) {
    return request({
      url: `${LOG_BASE_URL}/${id}`,
      method: "put",
      data: data,
    });
  }

  static add(data: LogStoreForm) {
    return request({
      url: `${LOG_BASE_URL}/create`,
      method: "post",
      data: data,
    });
  }
}

export default LogsStoreAPI;

export interface LogStoreForm {
  create_time?: Date;
  store?: string;
  name?: string;
  connect_url?: string;
  id?: number;
  status?: number;
  sort?: number;
}

/**
 * 日志分页查询对象
 */
export interface LogsStorePageQuery extends PageQuery {
  /** 搜索关键字 */
  keywords?: string;
}

/**
 * 系统日志分页VO
 */
export interface LogsStorePageVO {
  /** 主键 */
  id: number;
  store: string;
  name: string;
  status: number;
  sort: number;
}
