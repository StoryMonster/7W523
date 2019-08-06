
#删除所有pyc文件
Get-ChildItem ..\..\Server -recurse *.pyc | Remove-Item -Force