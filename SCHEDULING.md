# Scheduling Setup - Silver Tier

This guide explains how to set up automated scheduling for your AI Employee.

## Windows Setup (Task Scheduler)

### Option 1: Task Scheduler GUI

1. **Open Task Scheduler**:
   - Press `Win + R`
   - Type `taskschd.msc`
   - Press Enter

2. **Create Basic Task**:
   - Click "Create Basic Task" in right sidebar
   - Name: `AI Employee Daily Tasks`
   - Description: `Run AI Employee scheduled tasks daily`
   - Click Next

3. **Trigger**:
   - Select "Daily"
   - Click Next

4. **Daily Settings**:
   - Start date: Today
   - Start time: `9:00:00 AM` (or your preferred time)
   - Recur every: 1 day
   - Click Next

5. **Action**:
   - Select "Start a program"
   - Click Next

6. **Program/Script**:
   - Program/script: `C:\HACKATHON 0\schedule_tasks.bat`
   - Start in: `C:\HACKATHON 0`
   - Click Next

7. **Finish**:
   - Review settings
   - Click "Finish"

### Option 2: Command Line

Open Command Prompt as Administrator:

```cmd
schtasks /create /tn "AI Employee Daily Tasks" /tr "C:\HACKATHON 0\schedule_tasks.bat" /sc daily /st 09:00
```

To verify:
```cmd
schtasks /query /tn "AI Employee Daily Tasks"
```

To run manually:
```cmd
schtasks /run /tn "AI Employee Daily Tasks"
```

To delete:
```cmd
schtasks /delete /tn "AI Employee Daily Tasks" /f
```

## Linux/Mac Setup (Cron)

### Edit Crontab

```bash
crontab -e
```

### Add Cron Job

Run daily at 9:00 AM:
```cron
0 9 * * * cd /path/to/HACKATHON\ 0 && ./schedule_tasks.sh >> ai_employee.log 2>&1
```

### Cron Format

```
* * * * * command
│ │ │ │ │
│ │ │ │ └─── Day of week (0-7, Sunday = 0 or 7)
│ │ │ └───── Month (1-12)
│ │ └─────── Day of month (1-31)
│ └───────── Hour (0-23)
└─────────── Minute (0-59)
```

### Examples

Every hour:
```cron
0 * * * * cd /path/to/HACKATHON\ 0 && ./schedule_tasks.sh
```

Every 6 hours:
```cron
0 */6 * * * cd /path/to/HACKATHON\ 0 && ./schedule_tasks.sh
```

Every Monday at 9 AM:
```cron
0 9 * * 1 cd /path/to/HACKATHON\ 0 && ./schedule_tasks.sh
```

## Verify Scheduling

### Check Log File

```bash
# Windows
type ai_employee.log

# Linux/Mac
tail -f ai_employee.log
```

### Manual Test

Run the scheduled task script manually to verify it works:

```bash
# Windows
schedule_tasks.bat

# Linux/Mac
chmod +x schedule_tasks.sh
./schedule_tasks.sh
```

## What Gets Scheduled

The scheduled task runner performs these actions:

1. **Generate Plans**: Analyzes tasks in Needs_Action and creates Plan.md for complex ones
2. **Process Tasks**: Executes pending tasks autonomously
3. **Update Dashboard**: Refreshes system state visualization
4. **Check Approvals**: Reports statistics on approval workflow

## Troubleshooting

### Task Not Running

- Verify the script path is correct
- Check Task Scheduler history (right-click task → "View History")
- Ensure virtual environment is activated in script
- Check log file for errors

### Permission Errors

- Run Task Scheduler with highest privileges
- On Linux/Mac, ensure script is executable: `chmod +x schedule_tasks.sh`

### Python Not Found

- Use absolute paths in script
- Ensure virtual environment path is correct
- Test by running script manually first

## Next Steps

Once scheduling is set up:
- ✅ Your AI Employee runs automatically
- ✅ Tasks are processed without manual intervention
- ✅ Dashboard stays up to date
- ✅ Silver tier scheduling requirement met!

---

**Silver Tier Requirement**: ✅ Automated daily/weekly scheduling demonstrated
