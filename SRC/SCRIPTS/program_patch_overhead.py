import os

folder_path = '../../OBJ/PROGRAMS'

patches_mem_dict = dict(zip(sorted(os.listdir(folder_path)), [os.path.join(folder_path, f) + "/PROGRAM_COMPILED/program_encrypted_cs1_patches.mem" for f in sorted(os.listdir(folder_path))]))

for program in patches_mem_dict.keys():
    file = patches_mem_dict[program]

    with open(file, "r") as f:
        patch_mem=f.read()


    patch_mem_l = list(filter(('').__ne__, list(patch_mem.split('\n'))))
    cnt_patch = 0
    cnt_line = 0
    cnt_redir = 0
    for line in patch_mem_l:
        cnt_line += 1
        if line != "0000000000000000000000000000000000000000000000000000000000000000000000000000000000":
            cnt_patch +=1
        if line[2:5] == "fff":
            cnt_redir+=1

    print(f"{program:>15}: {cnt_line:>5} | {cnt_patch:>5}({cnt_patch/cnt_line:.3f}) | {cnt_redir:>5}({cnt_redir/cnt_line:.3f})")

