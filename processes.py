
import os
import sys
import re
import subprocess
import collections

class ProcessTable():
  def __init__(self, procs):
    by_pid = {}
    parent_pid = {}
    child_pids = collections.defaultdict(set)

    for p in procs:
      pid = p['PID']
      ppid = p['PPID']
      by_pid[ pid ] = p
      parent_pid[ pid ] = ppid
      child_pids[ ppid ].add(pid)

    self.by_pid = by_pid
    self.parent_pid = parent_pid
    self.child_pids = child_pids

  def all_pids(self):
    return self.by_pid.keys()

  def ppid(self, pid):
    return self.parent_pid.get(pid, None)

  def children(self, pid):
    if pid in self.child_pids:
      return self.child_pids[pid]
    else:
      return set()

  def attr(self, key, pid):
    proc = self.by_pid.get(pid, None)
    if proc:
      return proc.get(key, None)
    return None

  def command(self, pid):
    return self.attr('COMMAND', pid)

  def root(self, pid):
    """Return the root of the process tree for this pid."""
    seen = set()
    while pid not in seen:
      seen.add(pid)
      ppid = self.ppid(pid)
      if ppid is None: return pid
      pid = ppid
    return None

def ptable_roots(ptable):
  """Return the top-level processes"""
  allpids = set( ptable.all_pids() )
  roots = []
  for pid in allpids:
    ppid = ptable.ppid( pid )
    if ppid not in allpids:
      roots.append(pid)
  return roots

def parse_ps_output(text):
  """Parse the output of ps and return a list of dictionaries."""
  lines = text.split('\n')
  header = lines[0]
  colnames = header.split()
  ncols = len(colnames)
  procs = []
  # print "ncols:", ncols, "colnames:", colnames

  for x in lines[1:]:
    cols = x.split(None, ncols-1)
    p = {}
    for i,v in enumerate(cols):
      if i >= ncols: print "bad cols:", cols
      p[ colnames[i] ] = v
      procs.append(p)
  return procs

def capture_output(cmd):
  """Run a command and return its output."""
  return subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]

def make_process_table(cmd):
  """Return a ProcessTable and list of parsed processes from the output of a ps command.
     cmd is typically something like ['ps', 'axo', 'pid,ppid,command']
  """
  ps_output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
  procs = parse_ps_output(ps_output)
  ptable = ProcessTable(procs)
  return (ptable, procs)

def process_cwd(pid):
  """Return the process current working directory."""
  path = "/proc/{}/cwd".format(pid)
  try:
    return os.readlink(path)
  except:
    return None


