param(
    [string]$ImageName = "ainewsback",
    [string]$Tag = "v1.1.0",
    [string]$DockerUser = "acdb24",
    [string]$DockerPassword = ""
)

$FullImage = "$DockerUser/$ImageName`:$Tag"

if (-not $DockerPassword) {
    $SecurePwd = Read-Host -AsSecureString "请输入 Docker Hub 密码"
    $PlainPwd = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecurePwd)
    )
} else {
    $PlainPwd = $DockerPassword
}

Write-Host "==> 登录 Docker Hub"
$PlainPwd | docker login -u $DockerUser --password-stdin
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$ProjectRoot = Resolve-Path "$PSScriptRoot\.."
$DockerfilePath = "$ProjectRoot\Dockerfile"

Write-Host "==> 构建镜像: $FullImage"
docker build -t $FullImage -f $DockerfilePath $ProjectRoot
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "==> 推送镜像: $FullImage"
docker push $FullImage
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "==> 完成"