# ImmortalWrt 镜像运行指南

## 镜像文件说明

从您的编译输出可以看到有以下类型的镜像文件：

### 磁盘镜像格式
- **`.img.gz`** - 压缩的原始磁盘镜像
- **`.qcow2.gz`** - 压缩的 QEMU 镜像
- **`.vdi.gz`** - 压缩的 VirtualBox 镜像  
- **`.vhdx.gz`** - 压缩的 Hyper-V 镜像
- **`.vmdk.gz`** - 压缩的 VMware 镜像

### 启动镜像
- **`.iso`** - 可启动光盘镜像

### 文件系统
- **`rootfs.tar.gz`** - 根文件系统压缩包
- **`kernel.bin`** - 内核文件

## 运行方法

### 1. 解压镜像文件
首先需要解压压缩的镜像文件：

```bash
# 解压 .gz 文件
gunzip immortalwrt-23.05-snapshot-r28342-6020ee24fa-x86-64-generic-ext4-combined-efi.img.gz
gunzip immortalwrt-23.05-snapshot-r28342-6020ee24fa-x86-64-generic-ext4-combined-efi.qcow2.gz
# 其他格式类似
```

### 2. 使用 QEMU 运行（推荐）

#### 运行 .img 镜像
```bash
# 基本运行
qemu-system-x86_64 \
  -m 512M \
  -smp 2 \
  -drive file=immortalwrt-23.05-snapshot-r28342-6020ee24fa-x86-64-generic-ext4-combined.img,format=raw \
  -netdev user,id=wan,hostfwd=tcp::2222-:22 \
  -device virtio-net-pci,netdev=wan \
  -nographic

# 带 EFI 支持的镜像
qemu-system-x86_64 \
  -m 512M \
  -smp 2 \
  -bios /usr/share/ovmf/OVMF.fd \
  -drive file=immortalwrt-23.05-snapshot-r28342-6020ee24fa-x86-64-generic-ext4-combined-efi.img,format=raw \
  -netdev user,id=wan,hostfwd=tcp::2222-:22 \
  -device virtio-net-pci,netdev=wan \
  -nographic
```

#### 运行 .qcow2 镜像
```bash
qemu-system-x86_64 \
  -m 512M \
  -smp 2 \
  -drive file=immortalwrt-23.05-snapshot-r28342-6020ee24fa-x86-64-generic-ext4-combined-efi.qcow2,format=qcow2 \
  -netdev user,id=wan,hostfwd=tcp::2222-:22 \
  -device virtio-net-pci,netdev=wan \
  -nographic
```

#### 运行 ISO 镜像
```bash
qemu-system-x86_64 \
  -m 512M \
  -smp 2 \
  -cdrom immortalwrt-23.05-snapshot-r28342-6020ee24fa-x86-64-generic-image-efi.iso \
  -boot d \
  -netdev user,id=wan,hostfwd=tcp::2222-:22 \
  -device virtio-net-pci,netdev=wan \
  -nographic
```

### 3. 使用 VirtualBox 运行

1. 创建新的虚拟机
2. 类型选择 "Linux"，版本选择 "Other Linux (64-bit)"
3. 内存设置为 512MB
4. 选择 "使用已有的虚拟硬盘文件"
5. 选择解压后的 `.vdi` 文件
6. 启动虚拟机

### 4. 使用 VMware 运行

1. 创建新的虚拟机
2. 选择 "自定义"
3. 选择解压后的 `.vmdk` 文件作为磁盘
4. 配置网络为 NAT 模式
5. 启动虚拟机

### 5. 使用 Hyper-V 运行

1. 创建新的虚拟机
2. 选择第二代
3. 使用现有的虚拟硬盘，选择 `.vhdx` 文件
4. 配置网络
5. 启动虚拟机

## 网络配置说明

在 QEMU 命令中，`hostfwd=tcp::2222-:22` 表示将宿主机的 2222 端口转发到虚拟机的 22 端口（SSH）。

启动后可以通过 SSH 连接：
```bash
ssh root@localhost -p 2222
```

默认密码通常是空密码或 "password"。

## 推荐的运行方式

### 最简单的方式 - 使用 QEMU 运行 ISO
```bash
# 直接运行 ISO 镜像，无需解压
qemu-system-x86_64 \
  -m 512M \
  -smp 2 \
  -cdrom immortalwrt-23.05-snapshot-r28342-6020ee24fa-x86-64-generic-image-efi.iso \
  -boot d \
  -netdev user,id=wan,hostfwd=tcp::2222-:22,hostfwd=tcp::8080-:80 \
  -device virtio-net-pci,netdev=wan \
  -nographic
```

### 带图形界面的运行
去掉 `-nographic` 参数即可显示图形界面：
```bash
qemu-system-x86_64 \
  -m 512M \
  -smp 2 \
  -cdrom immortalwrt-23.05-snapshot-r28342-6020ee24fa-x86-64-generic-image-efi.iso \
  -boot d \
  -netdev user,id=wan,hostfwd=tcp::2222-:22,hostfwd=tcp::8080-:80 \
  -device virtio-net-pci,netdev=wan
```

## 故障排除

1. **QEMU 未安装**：
   ```bash
   # Ubuntu/Debian
   sudo apt install qemu-system-x86
   
   # CentOS/RHEL
   sudo yum install qemu-kvm
   ```

2. **EFI BIOS 文件缺失**：
   ```bash
   # Ubuntu/Debian
   sudo apt install ovmf
   ```

3. **网络连接问题**：
   检查端口转发配置，确保防火墙未阻止连接。

4. **内存不足**：
   如果启动失败，尝试增加内存到 1GB 或更多。
