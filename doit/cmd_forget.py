from .cmd_base import DoitCmdBase, check_tasks_exist
from .cmd_base import tasks_and_deps_iter, subtasks_iter


opt_forget_taskdep = {
    'name': 'forget_sub',
    'short': 's',
    'long': 'follow-sub',
    'type': bool,
    'default': False,
    'help': 'forget task dependencies too',
    }

opt_forget_all = {
    'name': 'forget_all',
    'short': 'a',
    'long': 'all',
    'type': bool,
    'default': False,
    'help': 'forget all tasks',
    }


class Forget(DoitCmdBase):
    doc_purpose = "clear successful run status from internal DB"
    doc_usage = "[TASK ...]"
    doc_description = None

    cmd_options = (opt_forget_taskdep, opt_forget_all)

    def _execute(self, forget_sub, forget_all):
        """remove saved data successful runs from DB
        """
        # no task specified. forget all if user requests it
        if not self.sel_tasks and forget_all:
            self.dep_manager.remove_all()
            self.outstream.write("forgetting all tasks\n")

        elif not self.sel_tasks:
             self.outstream.write(
                 "no tasks specified, pass --all to forget all tasks\n")

        # forget tasks from list
        else:
            tasks = dict([(t.name, t) for t in self.task_list])
            check_tasks_exist(tasks, self.sel_tasks)
            forget_list = self.sel_tasks

            if forget_sub:
                to_forget = list(tasks_and_deps_iter(tasks, forget_list, True))
            else:
                to_forget = []
                for name in forget_list:
                    task = tasks[name]
                    to_forget.append(task)
                    to_forget.extend(subtasks_iter(tasks, task))

            for task in to_forget:
                # forget it - remove from dependency file
                self.dep_manager.remove(task.name)
                self.outstream.write("forgetting %s\n" % task.name)
        self.dep_manager.close()
