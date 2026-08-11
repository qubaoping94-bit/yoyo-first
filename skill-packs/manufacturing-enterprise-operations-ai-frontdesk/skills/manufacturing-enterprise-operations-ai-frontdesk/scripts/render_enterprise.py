import hashlib,json,re,sys
from pathlib import Path
p=Path(sys.argv[1]);o=Path(sys.argv[2]);d=json.loads(p.read_text("utf-8"));SCHEMA="A-MFG-PROFILE-1.1.0"
missing=[]
from datetime import datetime
if not isinstance(d,dict):d={"conflicts":["top_level(object)"]}
if not isinstance(d.get("enterprise"),dict):d["enterprise"]={}
for k in ("name","business_type","timezone","currency"):
 if not isinstance(d["enterprise"].get(k),str):d["enterprise"][k]=""
for key in ("products_and_units","employees_roles_permissions","source_evidence","customers_projects"):
 if not isinstance(d.get(key),list) or any(not isinstance(x,dict) for x in d.get(key,[])):d[key]=[]
for x in d.get("products_and_units",[]):
 for k in ("product_id","name","specification","unit","price_policy"):
  if not isinstance(x.get(k),str):x[k]=""
for x in d.get("employees_roles_permissions",[]):
 for k in ("account_id","display_name","role"):
  if not isinstance(x.get(k),str):x[k]=""
 if not isinstance(x.get("permissions"),list) or not all(isinstance(y,str) and y for y in x.get("permissions",[])):x["permissions"]=[]
accounts=[x.get("account_id") for x in d.get("employees_roles_permissions",[])]
if any(x and accounts.count(x)>1 for x in accounts):d["employees_roles_permissions"]=[]
for x in d.get("source_evidence",[]):
 if not isinstance(x.get("sha256"),str) or not re.fullmatch(r"[0-9A-Fa-f]{64}",x.get("sha256","")):x["sha256"]=""
 for k in ("source","extracted_at"):
  if not isinstance(x.get(k),str):x[k]=""
if not isinstance(d.get("enabled_workflows"),list) or not d.get("enabled_workflows") or not all(isinstance(x,str) and x for x in d.get("enabled_workflows",[])):d["enabled_workflows"]=[]
if not isinstance(d.get("external_interfaces"),dict) or not d.get("external_interfaces") or not all(isinstance(k,str) and isinstance(v,str) and v for k,v in d.get("external_interfaces",{}).items()):d["external_interfaces"]={}
if not isinstance(d.get("numbering_rules"),dict):d["numbering_rules"]={}
for k in ("order","production"):
 if not isinstance(d["numbering_rules"].get(k),str):d["numbering_rules"][k]=""
if not isinstance(d.get("suppliers_warehouses_logistics"),dict):d["suppliers_warehouses_logistics"]={}
for key in ("suppliers","warehouses","logistics"):
 v=d["suppliers_warehouses_logistics"].get(key)
 if not isinstance(v,list) or any(not isinstance(x,dict) or not isinstance(x.get("id"),str) or not x.get("id") or not isinstance(x.get("name"),str) or not x.get("name") for x in v):d["suppliers_warehouses_logistics"][key]=[]
if any(not all(isinstance(x.get(k),str) and x.get(k) for k in ("customer_id","customer_name","project_id","project_name","order_seed")) for x in d.get("customers_projects",[])):d["customers_projects"]=[]
if not isinstance(d.get("conflicts"),list):d["conflicts"]=["conflicts(array)"]
if not isinstance(d.get("confirmation"),dict):d["confirmation"]={}
for k in ("status","confirmed_by_account_id","display_name_snapshot","role_snapshot","confirmed_at","source_profile_version","source_sha256"):
 if not isinstance(d["confirmation"].get(k),str):d["confirmation"][k]=""
try:
 _dt=datetime.fromisoformat(str(d["confirmation"].get("confirmed_at","")).replace("Z","+00:00"))
 if _dt.tzinfo is None:d["confirmation"]["confirmed_at"]=""
except Exception:d["confirmation"]["confirmed_at"]=""
def req(obj,key,path):
 v=obj.get(key) if isinstance(obj,dict) else None
 if v is None or v=="" or v==[] or v=={}:missing.append(path)
 return v
ent=d.get("enterprise",{});[req(ent,k,"enterprise."+k) for k in ("name","business_type","timezone","currency")]
products=d.get("products_and_units",[])
if not products:missing.append("products_and_units[0]")
else:
 for i,x in enumerate(products):
  for k in ("product_id","name","specification","unit","price_policy"):req(x,k,f"products_and_units[{i}].{k}")
employees=d.get("employees_roles_permissions",[])
if not employees:missing.append("employees_roles_permissions[0]")
else:
 for i,x in enumerate(employees):
  for k in ("account_id","display_name","role","permissions"):req(x,k,f"employees_roles_permissions[{i}].{k}")
rules=d.get("numbering_rules",{});req(rules,"order","numbering_rules.order");req(rules,"production","numbering_rules.production");req(d,"enabled_workflows","enabled_workflows");req(d,"external_interfaces","external_interfaces")
flows=d.get("enabled_workflows",[]);swl=d.get("suppliers_warehouses_logistics",{});conditional={"采购":("suppliers","suppliers_warehouses_logistics.suppliers"),"仓储":("warehouses","suppliers_warehouses_logistics.warehouses"),"交付":("logistics","suppliers_warehouses_logistics.logistics"),"订单":("customers_projects","customers_projects")}
for flow,(key,path) in conditional.items():
 if flow in flows and not (d.get(key) if key=="customers_projects" else swl.get(key)):missing.append(path)
evidence=d.get("source_evidence",[])
if not evidence:missing.append("source_evidence[0]")
else:
 for i,x in enumerate(evidence):
  for k in ("sha256","source","extracted_at"):req(x,k,f"source_evidence[{i}].{k}")
  if x.get("sha256") and not re.fullmatch(r"[0-9A-Fa-f]{64}",x["sha256"]):missing.append(f"source_evidence[{i}].sha256(valid)")
conf=d.get("confirmation",{});account=conf.get("confirmed_by_account_id");person=next((x for x in employees if x.get("account_id")==account),None);permission_ok=bool(person and "企业启用确认" in person.get("permissions",[]) and conf.get("display_name_snapshot")==person.get("display_name") and conf.get("role_snapshot")==person.get("role"));evidence_sha={x.get("sha256") for x in evidence if isinstance(x,dict)};confirmation_ok=conf.get("status")=="CONFIRMED" and bool(conf.get("confirmed_at")) and conf.get("source_profile_version")==d.get("profile_version") and conf.get("source_sha256") in evidence_sha and permission_ok
schema_ok=d.get("enterprise_profile_schema_version")==SCHEMA;scope=d.get("data_scope");scope_ok=scope in ("DEMO","FORMAL");ready=schema_ok and scope_ok and not missing and not d.get("conflicts",[]) and confirmation_ok;mode=("DEMO" if scope=="DEMO" else "LIVE") if ready else "SETUP"
reason=None if ready else ("PERMISSION_DENIED" if conf.get("status")=="CONFIRMED" and not permission_ok else "SETUP_INCOMPLETE")
idempotency_material=f"{ent.get('name','')}|{d.get('profile_version','')}|{conf.get('source_sha256','')}";idem=hashlib.sha256(idempotency_material.encode()).hexdigest().upper()
base={"enterprise_profile_schema_version":d.get("enterprise_profile_schema_version"),"profile_version":d.get("profile_version"),"data_scope":scope,"mode":mode,"activation_status":reason or "READY","formal_write_count":0,"formal_records":[],"missing_fields":sorted(set(missing)),"conflicts":d.get("conflicts",[]),"schema_error":None if schema_ok else f"expected {SCHEMA}","confirmation_authorized":permission_ok,"confirmation_snapshot":conf,"permission_profiles":employees,"activation_idempotency_key":idem}
if ready:
 product=products[0];cp=(d.get("customers_projects") or [{}])[0];order=cp.get("order_seed",rules["order"]);base.update({"enterprise_master":{"name":ent["name"],"business_type":ent["business_type"],"product":product["name"],"specification":product["specification"],"unit":product["unit"]},"numbering_rules":rules,"titles":[f"业务｜{order}｜{cp.get('customer_name','待关联客户')}",f"生产｜{order}｜{product['name']}｜{product['unit']}"],"record_skeleton":{"order":order,"owner_account":person["account_id"],"owner":person["display_name"],"product_id":product["product_id"],"customer_id":cp.get("customer_id"),"project_id":cp.get("project_id"),"activation_only":True}})
else:base["setup_preview"]={"message":"企业资料尚未完整或未获授权确认；这里只生成启用预览，不创建正式记录。","next_action":"补齐缺项、处理冲突，并由员工权限中包含‘企业启用确认’的账号确认。","enterprise":ent,"products_and_units":products,"employees_roles_permissions":employees,"enabled_workflows":flows,"numbering_rules":rules,"external_interfaces":d.get("external_interfaces",{})}
o.write_text(json.dumps(base,ensure_ascii=False,indent=2),"utf-8");print(str(o))
