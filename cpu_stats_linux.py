
# read CPU stats routines for Linux

import collections

CpuStats = collections.namedtuple("CpuStats", ["user", "nice", "system", "idle", "iowait", "irq", "softirq"])

# cpu  17250565 3052 1331470 14714068 24588 0 5740 674219 0 0

def cpu_stats():
  with open("/proc/stat") as f:
    output = f.readline()
  ws = [ int(w) for w in output.split()[1:] ]
  stats = CpuStats( user=ws[0], nice=ws[1], system=ws[2], idle=ws[3], iowait=ws[4], irq=ws[5], softirq=ws[6])
  return stats

def diff_stats(a,b):
  c = CpuStats(user=a.user-b.user,nice=a.nice-b.nice,system=a.system-b.system,idle=a.idle-b.idle,iowait=a.iowait-b.iowait,irq=a.irq-b.irq,softirq=a.softirq-b.softirq)
  return c

def idle_percent(st):
  total = st.user+st.nice+st.system+st.idle+st.iowait+st.irq+st.softirq
  return st.idle / float(total)

