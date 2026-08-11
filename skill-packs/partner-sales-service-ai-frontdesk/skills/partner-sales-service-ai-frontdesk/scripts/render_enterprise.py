import hashlib,json,re,sys
from datetime import datetime
from pathlib import Path
inp=Path(sys.argv[1]);out=Path(sys.argv[2]);SCHEMA="B-PARTNER-PROFILE-1.0.0"
try:d=json.loads(inp.read_text("utf-8"))
except Exception:d={}
top_bad=not isinstance(d,dict)
if top_bad:d={}
issues=["top_level(object)"] if top_bad else []
def obj(v,path):
 if not isinstance(v,dict):issues.append(path+"(object)");return {}
 return v
def arr(v,path):
 if not isinstance(v,list):issues.append(path+"(array)");return []
 return v
def val(o,k,path):
 v=o.get(k) if isinstance(o,dict) else None
 if not isinstance(v,str) or not v:issues.append(path+"(string)")
 return v
def dict_items(v,path):
 a=arr(v,path);out=[]
 for i,x in enumerate(a):
  if not isinstance(x,dict):issues.append(f"{path}[{i}](object)")
  else:out.append(x)
 return out
ent=obj(d.get("enterprise"),"enterprise");[val(ent,k,"enterprise."+k) for k in ("name","business_type","timezone","currency")]
offers=dict_items(d.get("offerings"),"offerings")
if not offers:issues.append("offerings[0]")
for i,x in enumerate(offers):
 for k in ("offering_id","name","specification","unit","price_policy"):val(x,k,f"offerings[{i}].{k}")
emps=dict_items(d.get("employees_roles_permissions"),"employees_roles_permissions")
if not emps:issues.append("employees_roles_permissions[0]")
accounts=[]
for i,x in enumerate(emps):
 for k in ("account_id","display_name","role"):val(x,k,f"employees_roles_permissions[{i}].{k}")
 perms=x.get("permissions")
 if not isinstance(perms,list) or not all(isinstance(y,str) and y for y in perms):issues.append(f"employees_roles_permissions[{i}].permissions(list[str])")
 accounts.append(x.get("account_id"))
if any(x and accounts.count(x)>1 for x in accounts):issues.append("employees_roles_permissions.account_id(unique)")
rules=obj(d.get("numbering_rules"),"numbering_rules");[val(rules,k,"numbering_rules."+k) for k in ("quote","order","receipt","shipment","aftersale")]
flows=d.get("enabled_workflows");allowed={"合作商","客户项目","报价","订单","付款凭证","实际到账","备货","交付","签收验收","欠款","售后回访","仓储"}
if not isinstance(flows,list) or not flows or not all(isinstance(x,str) and x in allowed for x in flows):issues.append("enabled_workflows(nonempty known list[str])");flows=flows if isinstance(flows,list) else []
interfaces=d.get("external_interfaces")
if not isinstance(interfaces,dict) or not interfaces or not all(isinstance(k,str) and isinstance(v,str) and v for k,v in interfaces.items()):issues.append("external_interfaces(object[str,str])");interfaces=interfaces if isinstance(interfaces,dict) else {}
partners=dict_items(d.get("partners"),"partners");cps=dict_items(d.get("customers_projects"),"customers_projects");ful=obj(d.get("fulfillment"),"fulfillment");points=dict_items(ful.get("receiving_points"),"fulfillment.receiving_points");ware=dict_items(ful.get("warehouses"),"fulfillment.warehouses");carriers=dict_items(ful.get("carriers"),"fulfillment.carriers")
for i,x in enumerate(partners):
 for k in ("partner_id","partner_name"):val(x,k,f"partners[{i}].{k}")
for i,x in enumerate(cps):
 for k in ("customer_id","customer_name","project_id","project_name","order_seed"):val(x,k,f"customers_projects[{i}].{k}")
for label,items in (("receiving_points",points),("warehouses",ware),("carriers",carriers)):
 for i,x in enumerate(items):
  for k in ("id","name"):val(x,k,f"fulfillment.{label}[{i}].{k}")
if "合作商" in flows and (not partners or any(not x.get("partner_id") or not x.get("partner_name") for x in partners)):issues.append("conditional.合作商")
if "客户项目" in flows and (not cps or any(not all(x.get(k) for k in ("customer_id","customer_name","project_id","project_name","order_seed")) for x in cps)):issues.append("conditional.客户项目")
if "交付" in flows and (not points or not carriers or any(not x.get("id") or not x.get("name") for x in points+carriers)):issues.append("conditional.交付")
if "仓储" in flows and (not ware or any(not x.get("id") or not x.get("name") for x in ware)):issues.append("conditional.仓储")
evidence=dict_items(d.get("source_evidence"),"source_evidence")
if not evidence:issues.append("source_evidence[0]")
for i,x in enumerate(evidence):
 for k in ("sha256","source","extracted_at"):val(x,k,f"source_evidence[{i}].{k}")
 if not isinstance(x.get("sha256"),str) or not re.fullmatch(r"[0-9A-Fa-f]{64}",x.get("sha256","")):issues.append(f"source_evidence[{i}].sha256(valid string)")
conf=obj(d.get("confirmation"),"confirmation")
for k in ("status","confirmed_by_account_id","display_name_snapshot","role_snapshot","confirmed_at","source_profile_version","source_sha256"):val(conf,k,"confirmation."+k)
acct=conf.get("confirmed_by_account_id");matches=[x for x in emps if x.get("account_id")==acct];person=matches[0] if len(matches)==1 else None;perms=person.get("permissions") if person else None;permission_ok=bool(person and isinstance(perms,list) and all(isinstance(x,str) for x in perms) and "企业启用确认" in perms and conf.get("display_name_snapshot")==person.get("display_name") and conf.get("role_snapshot")==person.get("role"))
time_ok=False
try:
 dt=datetime.fromisoformat(str(conf.get("confirmed_at","")).replace("Z","+00:00"));time_ok=dt.tzinfo is not None
except Exception:pass
if conf.get("status")=="CONFIRMED" and not time_ok:issues.append("confirmation.confirmed_at(timezone ISO8601)")
esh={x.get("sha256") for x in evidence if isinstance(x.get("sha256"),str)};confirmed=conf.get("status")=="CONFIRMED" and permission_ok and time_ok and conf.get("source_profile_version")==d.get("profile_version") and conf.get("source_sha256") in esh
schema_ok=d.get("enterprise_profile_schema_version")==SCHEMA;scope=d.get("data_scope");ready=schema_ok and scope in ("DEMO","FORMAL") and not issues and isinstance(d.get("conflicts"),list) and not d.get("conflicts") and confirmed;mode=("DEMO" if scope=="DEMO" else "LIVE") if ready else "SETUP";result={"enterprise_profile_schema_version":d.get("enterprise_profile_schema_version"),"profile_version":d.get("profile_version"),"data_scope":scope,"mode":mode,"activation_status":"READY" if ready else ("PERMISSION_DENIED" if conf.get("status")=="CONFIRMED" and not permission_ok else "SETUP_INCOMPLETE"),"confirmation_authorized":permission_ok,"missing_fields":sorted(set(issues)),"conflicts":d.get("conflicts") if isinstance(d.get("conflicts"),list) else ["conflicts(array)"],"formal_write_count":0,"formal_records":[],"activation_idempotency_key":hashlib.sha256(f"{ent.get('name','')}|{d.get('profile_version','')}|{conf.get('source_sha256','')}".encode()).hexdigest().upper()}
if ready:
 x=offers[0];cp=cps[0] if cps else {};order=cp.get("order_seed",rules["order"]);result.update({"enterprise_master":{"name":ent["name"],"offering":x["name"],"specification":x["specification"],"unit":x["unit"]},"numbering_rules":rules,"titles":[f"合作商客户｜{cp.get('customer_name','待关联客户')}",f"报价｜{rules['quote']}",f"订单｜{order}",f"到账｜{rules['receipt']}",f"发货物流｜{rules['shipment']}",f"售后回访｜{rules['aftersale']}"],"record_skeleton":{"partner_id":partners[0].get("partner_id") if partners else None,"customer_id":cp.get("customer_id"),"project_id":cp.get("project_id"),"offering_id":x["offering_id"],"quote_id":rules["quote"],"order_id":order,"payment_proof_id":"待本次凭证生成","actual_receipt_id":rules["receipt"],"stock_ready_status":"待已确认备货事件","shipment_id":rules["shipment"],"logistics_status":"待读取或上传凭证","sign_accept_status":"待签收验收事件","outstanding_amount":"按订单与实际到账计算","aftersale_id":rules["aftersale"],"activation_only":True}})
else:result["setup_preview"]={"enterprise":ent,"offerings":offers,"employees_roles_permissions":emps,"enabled_workflows":flows,"numbering_rules":rules,"external_interfaces":interfaces,"message":"只生成启用预览，不创建正式业务记录。"}
out.write_text(json.dumps(result,ensure_ascii=False,indent=2),"utf-8");print(str(out))
