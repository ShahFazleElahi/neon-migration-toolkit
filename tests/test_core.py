import tempfile,sqlite3,json,unittest
from pathlib import Path
from migrate import connect,inventory,export
class Test(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup); self.path=Path(self.tmp.name,'x.db')
  with sqlite3.connect(self.path) as db:
   db.execute('CREATE TABLE "odd name" (id INTEGER PRIMARY KEY, data BLOB, note TEXT)'); db.execute('INSERT INTO "odd name" VALUES (1,?,NULL)',(b'\x01',))
 def test_inventory(self):
  db=connect(self.path); self.addCleanup(db.close); self.assertEqual(inventory(db)[0]['row_count'],1)
 def test_export(self):
  out=self.path.parent/'export'; result=export(self.path,out); row=json.loads((out/result['tables'][0]['file']).read_text()); self.assertEqual(row,[1,{'type':'blob','base64':'AQ=='},None])
 def test_readonly(self):
  db=connect(self.path); self.addCleanup(db.close)
  with self.assertRaises(sqlite3.OperationalError): db.execute('DELETE FROM "odd name"')
 def test_no_overwrite(self):
  with self.assertRaises(FileExistsError): export(self.path,self.path.parent)
 def test_generated_column(self):
  with sqlite3.connect(self.path) as db:
   db.execute('CREATE TABLE generated (a INTEGER, b INTEGER GENERATED ALWAYS AS (a+1) STORED)'); db.execute('INSERT INTO generated(a) VALUES(5)')
  out=self.path.parent/'export'; t=next(x for x in export(self.path,out)['tables'] if x['name']=='generated'); self.assertEqual(json.loads((out/t['file']).read_text()),[5]); self.assertEqual(len(t['columns']),1)
