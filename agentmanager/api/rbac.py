# """Access Control Lists (ACL's) control access the API server."""
#
# from oslo_config import cfg
# from oslo_policy import policy
#
# from agentmanager.common import exception
#
# _ENFORCER = None
#
# CONF = cfg.CONF
#
#
# def reset():
#     global _ENFORCER
#     if _ENFORCER:
#         _ENFORCER.clear()
#         _ENFORCER = None
#
#
# def _has_rule(name):
#     return name in _ENFORCER.rules.keys()
#
#
# def enforce(policy_name, request, target={}):
#     """Checks authorization of a rule against the request and target.
#
#     :param request: HTTP request
#     :param policy_name: the policy name to validate authz against.
#     :param dict target: As much information about the object being operated
#                         on as possible.
#     """
#     global _ENFORCER
#     if not _ENFORCER:
#         _ENFORCER = policy.Enforcer(CONF)
#         _ENFORCER.load_rules()
#
#     rule_method = "agent:" + policy_name
#     headers = request.headers
#
#     policy_dict = dict()
#     policy_dict['roles'] = headers.get('X-Roles', "").split(",")
#     policy_dict['user_id'] = (headers.get('X-User-Id'))
#     policy_dict['user_name'] = (headers.get('X-User-Name'))
#     policy_dict['project_id'] = (headers.get('X-Project-Id'))
#     policy_dict['domain_id'] = (headers.get('X-Project-Domain-Id'))
#
#     if ((_has_rule('default') or _has_rule(rule_method)) and
#             not _ENFORCER.enforce(rule_method, target, policy_dict)):
#         raise exception.ForbiddenError("RBAC Authorization Failed")
#
#
# def get_limited_to(headers):
#     """Return the user and project the request should be limited to.
#
#     :param headers: HTTP headers dictionary
#     :return: A tuple of (user, project), set to None if there's no limit on
#     one of these.
#
#     """
#     global _ENFORCER
#     if not _ENFORCER:
#         _ENFORCER = policy.Enforcer(CONF)
#         _ENFORCER.load_rules()
#
#     policy_dict = dict()
#     policy_dict['roles'] = headers.get('X-Roles', "").split(",")
#     policy_dict['user_id'] = (headers.get('X-User-Id'))
#     policy_dict['user_name'] = (headers.get('X-User-Name'))
#     policy_dict['project_id'] = (headers.get('X-Project-Id'))
#     policy_dict['domain_id'] = (headers.get('X-Project-Domain-Id'))
#
#     rule_name = 'segregation' if _has_rule(
#         'segregation') else 'context_is_admin'
#     if not _ENFORCER.enforce(rule_name,
#                              {},
#                              policy_dict):
#         return headers.get('X-User-Id'), headers.get('X-Project-Id')
#
#     return None, None
#
#
# def get_limited_to_project(headers):
#     """Return the project the request should be limited to.
#
#     :param headers: HTTP headers dictionary
#     :return: A project, or None if there's no limit on it.
#
#     """
#     return get_limited_to(headers)[1]
