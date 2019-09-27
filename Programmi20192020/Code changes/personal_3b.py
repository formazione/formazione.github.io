# v. personal_3b ====================

# 1. personal_3b Changed 27/9/19 =====
class Ebook:
	# [...]
    def rename(self, filename):
        self.lstb.delete("active")
        os.rename(self.filename, "text\\" + filename)
        self.files = glob.glob("text\\*.txt")
        self.reload_list_files(filename)

# to
class Ebook:
	# [...]
    def rename(self, filename):
        self.lstb.delete("active")
        os.rename(self.filename, "text\\" + filename)
        self.files = glob.glob("text\\*.txt")
        self.reload_list_files(filename)

There was something strange
happening when I renamed files name,
it deleted the file, so I used
the reload_list_files function instead fo
# =============== version ======