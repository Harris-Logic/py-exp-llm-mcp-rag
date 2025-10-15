#!/bin/bash

# ImmortalWrt 运行脚本
# 这个脚本帮助您快速运行 ImmortalWrt 镜像

echo "=== ImmortalWrt 镜像运行助手 ==="
echo

# 检查 QEMU 是否安装
if ! command -v qemu-system-x86_64 &> /dev/null; then
    echo "❌ QEMU 未安装，正在尝试安装..."
    
    # 检测系统类型并安装 QEMU
    if command -v apt &> /dev/null; then
        sudo apt update
        sudo apt install -y qemu-system-x86
    elif command -v yum &> /dev/null; then
        sudo yum install -y qemu-kvm
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y qemu-kvm
    else
        echo "❌ 无法自动安装 QEMU，请手动安装："
        echo "Ubuntu/Debian: sudo apt install qemu-system-x86"
        echo "CentOS/RHEL: sudo yum install qemu-kvm"
        exit 1
    fi
fi

echo "✅ QEMU 已安装"

# 检查镜像文件
echo
echo "📁 检查可用的镜像文件..."

# 假设镜像文件在当前目录的 bin/targets/x86/64/ 目录下
IMAGE_DIR="bin/targets/x86/64"
ISO_FILE=""

if [ -d "$IMAGE_DIR" ]; then
    # 查找 ISO 文件
    ISO_FILE=$(find "$IMAGE_DIR" -name "*.iso" | head -1)
    
    if [ -n "$ISO_FILE" ]; then
        echo "✅ 找到 ISO 镜像: $ISO_FILE"
    else
        echo "❌ 未找到 ISO 镜像文件"
        echo "请确保在正确的目录运行此脚本"
        exit 1
    fi
else
    echo "❌ 镜像目录不存在: $IMAGE_DIR"
    echo "请确保在 ImmortalWrt 编译目录运行此脚本"
    exit 1
fi

echo
echo "🚀 准备启动 ImmortalWrt..."
echo "镜像文件: $ISO_FILE"
echo
echo "网络配置:"
echo "  - SSH: localhost:2222 -> 虚拟机:22"
echo "  - Web: localhost:8080 -> 虚拟机:80"
echo
echo "启动后可以通过以下方式连接:"
echo "  SSH: ssh root@localhost -p 2222"
echo "  Web: http://localhost:8080"
echo
echo "按 Ctrl+A 然后按 X 退出 QEMU"
echo

read -p "是否继续启动？(y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "取消启动"
    exit 0
fi

echo "正在启动 ImmortalWrt..."
echo "=========================================="

# 启动 QEMU
qemu-system-x86_64 \
    -m 512M \
    -smp 2 \
    -cdrom "$ISO_FILE" \
    -boot d \
    -netdev user,id=wan,hostfwd=tcp::2222-:22,hostfwd=tcp::8080-:80 \
    -device virtio-net-pci,netdev=wan \
    -nographic
