# Changelog

## 2019-08-29

- Add CPU usage limit.
- Allow the multi-image challenge.

Upgrade:
1. Execute this SQL in ctfd database.

```
alter table dynamic_docker_challenge add column cpu_limit float default 0.5 after memory_limit;
```  

2. Setting the containers you want to plugin to a single multi-image network. (In settings panel)

3. When you create a challenge you can set the docker image like this

```
{"socks": "serjs/go-socks5-proxy", "web": "blog_revenge_blog", "mysql": "blog_revenge_mysql", "oauth": "blog_revenge_oauth"}
```

The first one will be redirected the traffic.