import argparse, base64, json, sqlite3
from pathlib import Path

def quote(name): return '"'+name.replace('"','""')+'"'
def connect(path):
    return sqlite3.connect(Path(path).resolve().as_uri()+'?mode=ro',uri=True)
def inventory(db):
    names=[r[0] for r in db.execute("SELECT name FROM sqlite_schema WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
    return [{'name':n,'columns':[dict(zip(('cid','name','type','notnull','default','pk'),row)) for row in db.execute('PRAGMA table_info('+quote(n)+')')], 'foreign_keys':[list(r) for r in db.execute('PRAGMA foreign_key_list('+quote(n)+')')], 'row_count':db.execute('SELECT count(*) FROM '+quote(n)).fetchone()[0]} for n in names]
def encode(value):
    return {'type':'blob','base64':base64.b64encode(value).decode('ascii')} if isinstance(value,bytes) else value

def export(source, output):
    out=Path(output); out.mkdir(mode=0o700,parents=True,exist_ok=False)
    db=connect(source)
    try:
        db.execute('BEGIN'); tables=inventory(db)
        for i,t in enumerate(tables):
            t['file']=f'table-{i:04d}.jsonl'
            with (out/t['file']).open('x',encoding='utf-8') as f:
                for row in db.execute('SELECT '+','.join(quote(c['name']) for c in t['columns'])+' FROM '+quote(t['name'])):
                    f.write(json.dumps([encode(v) for v in row],ensure_ascii=False,allow_nan=False)+'\n')
        result={'format':1,'tables':tables,'warning':'Sensitive data. Review types and constraints before importing.'}
        (out/'manifest.json').write_text(json.dumps(result,indent=2),encoding='utf-8'); return result
    finally: db.close()

def main():
    p=argparse.ArgumentParser(); p.add_argument('source'); p.add_argument('--export-dir'); a=p.parse_args()
    if a.export_dir: result=export(a.source,a.export_dir)
    else:
        db=connect(a.source)
        try: result=inventory(db)
        finally: db.close()
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
