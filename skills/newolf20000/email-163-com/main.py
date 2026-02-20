#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
email-163-com - 163 邮箱完整邮件管理工具
版本：1.0.0
创建日期：2026-02-19
"""

import argparse
import smtplib
import imaplib
import email
import json
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import decode_header, Header
from email.utils import formataddr
import re
from datetime import datetime
import base64

# 默认配置
DEFAULT_CONFIG = {
    "email": "",
    "password": "",
    "imap_server": "imap.163.com",
    "imap_port": 993,
    "smtp_server": "smtp.163.com",
    "smtp_port": 465,
    "imap_id": {
        "name": "OpenClaw",
        "version": "1.0.0",
        "vendor": "email-163-com",
        "support_email": ""
    },
    "defaults": {
        "folder": "INBOX",
        "count": 5,
        "output_dir": "~/Downloads"
    }
}

CONFIG_PATH = os.path.expanduser("~/.config/email-163-com/config.json")


def remove_emoji(text):
    """移除字符串中的 emoji，避免邮件客户端显示问题"""
    if not text:
        return text
    # 匹配常见 emoji 范围
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # 表情符号
        "\U0001F300-\U0001F5FF"  # 符号和象形文字
        "\U0001F680-\U0001F6FF"  # 交通和地图符号
        "\U0001F1E0-\U0001F1FF"  # 国旗
        "\U00002702-\U000027B0"  # 装饰符号
        "\U000024C2-\U0001F251"  # 封闭符号
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub('', text).strip()


def load_config():
    """加载配置文件"""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
            # 合并默认配置
            for key in DEFAULT_CONFIG:
                if key not in config:
                    config[key] = DEFAULT_CONFIG[key]
            return config
    else:
        print(f"❌ 配置文件不存在：{CONFIG_PATH}")
        print("   请创建配置文件并填写邮箱信息")
        sys.exit(1)


def save_config(config):
    """保存配置文件"""
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    # 设置文件权限
    os.chmod(CONFIG_PATH, 0o600)
    print(f"✅ 配置文件已保存：{CONFIG_PATH}")


def init_config():
    """初始化配置"""
    print("📧 email-163-com 配置向导")
    print("=" * 50)
    
    config = DEFAULT_CONFIG.copy()
    config["defaults"] = DEFAULT_CONFIG["defaults"].copy()
    config["imap_id"] = DEFAULT_CONFIG["imap_id"].copy()
    
    # 获取邮箱地址
    email_addr = input(f"邮箱地址 [{config['email']}]: ").strip()
    if email_addr:
        config["email"] = email_addr
    
    # 获取授权码
    password = input("授权码（不是登录密码）: ").strip()
    if password:
        config["password"] = password
    
    # 保存配置
    save_config(config)
    print("\n✅ 配置完成！")
    print(f"   邮箱：{config['email']}")
    print(f"   IMAP: {config['imap_server']}:{config['imap_port']}")
    print(f"   SMTP: {config['smtp_server']}:{config['smtp_port']}")


def decode_mime_words(s):
    """解码 MIME 编码的字符串"""
    if not s:
        return ""
    decoded = []
    for part in decode_header(s):
        text, encoding = part
        if isinstance(text, bytes):
            try:
                decoded.append(text.decode(encoding or 'utf-8'))
            except:
                decoded.append(text.decode('utf-8', errors='replace'))
        else:
            decoded.append(text)
    return ''.join(decoded)


def send_email(args, config):
    """发送邮件"""
    try:
        # 创建邮件
        msg = MIMEMultipart()
        # 关键修复：使用 Header 编码中文标题和发件人，解决华为等客户端显示问题
        # 移除标题中的 emoji，避免华为客户端显示为横杠
        safe_subject = remove_emoji(args.subject)
        msg['From'] = formataddr((Header('OpenClaw 助手', 'utf-8').encode(), config['email']))
        msg['To'] = args.to
        msg['Subject'] = Header(safe_subject, 'utf-8')
        
        # 邮件正文
        if args.html:
            msg.attach(MIMEText(args.html, 'html', 'utf-8'))
        elif args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                msg.attach(MIMEText(f.read(), 'plain', 'utf-8'))
        else:
            msg.attach(MIMEText(args.body or '', 'plain', 'utf-8'))
        
        # 添加附件
        attachments = []
        if args.attach:
            for filepath in args.attach:
                if os.path.exists(filepath):
                    with open(filepath, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                    
                    encoders.encode_base64(part)
                    filename = os.path.basename(filepath)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename="{filename}"',
                    )
                    msg.attach(part)
                    attachments.append(filename)
                else:
                    print(f"⚠️  文件不存在：{filepath}")
        
        # 发送邮件
        server = smtplib.SMTP_SSL(config['smtp_server'], config['smtp_port'])
        server.login(config['email'], config['password'])
        server.sendmail(config['email'], args.to, msg.as_string())
        server.quit()
        
        print("✅ Message sent successfully!")
        print(f"   To: {args.to}")
        print(f"   Subject: {args.subject}")
        if attachments:
            print(f"   Attachments: {', '.join(attachments)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def read_emails(args, config):
    """读取邮件"""
    try:
        # 连接 IMAP
        mail = imaplib.IMAP4_SSL(config['imap_server'], config['imap_port'])
        mail.login(config['email'], config['password'])
        
        # 发送 IMAP ID（163 邮箱要求）
        imap_id = config['imap_id']
        id_str = f'("name" "{imap_id["name"]}" "version" "{imap_id["version"]}" "vendor" "{imap_id["vendor"]}" "support-email" "{imap_id["support_email"]}")'
        mail.xatom('ID', id_str)
        
        # 选择文件夹
        folder = args.folder or config['defaults']['folder']
        status, messages = mail.select(folder)
        if status != 'OK':
            print(f"❌ 无法选择文件夹：{folder}")
            return
        
        # 搜索邮件
        if args.unread:
            status, data = mail.search(None, 'UNSEEN')
        else:
            status, data = mail.search(None, 'ALL')
        
        if status != 'OK':
            print("❌ 无法搜索邮件")
            return
        
        msg_ids = data[0].split()
        total = len(msg_ids)
        count = args.count or config['defaults']['count']
        
        print(f"📬 {folder}: {total} messages total\n")
        
        if total == 0:
            print("   (没有邮件)")
            mail.close()
            mail.logout()
            return
        
        # 显示最新邮件
        for msg_id in msg_ids[-count:]:
            if args.full and args.id:
                # 读取完整邮件
                status, msg_data = mail.fetch(msg_id, '(RFC822)')
            else:
                # 只读取 header
                status, msg_data = mail.fetch(msg_id, '(RFC822.HEADER)')
            
            if status == 'OK':
                msg = email.message_from_bytes(msg_data[0][1])
                
                # 解码发件人
                from_header = decode_mime_words(msg.get('From', ''))
                
                # 解码主题
                subject = decode_mime_words(msg.get('Subject', ''))
                
                # 获取日期
                date = msg.get('Date', '')[:24]
                
                # 获取标志
                flags = msg.get('X-GM-LABELS', '')
                
                print(f"📧 From: {from_header}")
                print(f"   Subject: {subject}")
                print(f"   Date: {date}")
                print(f"   ID: {msg_id.decode()}")
                if flags:
                    print(f"   Flags: {flags}")
                print("-" * 50)
        
        mail.close()
        mail.logout()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def list_folders(args, config):
    """列出文件夹"""
    try:
        mail = imaplib.IMAP4_SSL(config['imap_server'], config['imap_port'])
        mail.login(config['email'], config['password'])
        
        # 发送 IMAP ID
        imap_id = config['imap_id']
        id_str = f'("name" "{imap_id["name"]}" "version" "{imap_id["version"]}" "vendor" "{imap_id["vendor"]}" "support-email" "{imap_id["support_email"]}")'
        mail.xatom('ID', id_str)
        
        status, folders = mail.list()
        if status == 'OK':
            print(f"📂 Found {len(folders)} folders:\n")
            for folder in folders:
                # 解码文件夹名
                decoded = folder.decode('utf-8', errors='replace')
                print(f"   - {decoded}")
        
        mail.logout()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def search_emails(args, config):
    """搜索邮件"""
    try:
        mail = imaplib.IMAP4_SSL(config['imap_server'], config['imap_port'])
        mail.login(config['email'], config['password'])
        
        # 发送 IMAP ID
        imap_id = config['imap_id']
        id_str = f'("name" "{imap_id["name"]}" "version" "{imap_id["version"]}" "vendor" "{imap_id["vendor"]}" "support-email" "{imap_id["support_email"]}")'
        mail.xatom('ID', id_str)
        
        # 选择文件夹
        folder = args.folder or config['defaults']['folder']
        mail.select(folder)
        
        # 构建搜索条件
        search_criteria = []
        if args.from_addr:
            search_criteria.append(f'FROM "{args.from_addr}"')
        if args.subject:
            search_criteria.append(f'SUBJECT "{args.subject}"')
        if args.to:
            search_criteria.append(f'TO "{args.to}"')
        
        if search_criteria:
            search_query = ' '.join(search_criteria)
        else:
            search_query = 'ALL'
        
        status, data = mail.search(None, search_query)
        if status != 'OK':
            print(f"❌ 搜索失败：{search_query}")
            return
        
        msg_ids = data[0].split()
        total = len(msg_ids)
        count = args.count or config['defaults']['count']
        
        print(f"🔍 Search: {search_query}")
        print(f"📬 Found: {total} messages\n")
        
        if total == 0:
            print("   (没有匹配的邮件)")
            mail.close()
            mail.logout()
            return
        
        # 显示匹配的邮件
        for msg_id in msg_ids[-count:]:
            status, msg_data = mail.fetch(msg_id, '(RFC822.HEADER)')
            if status == 'OK':
                msg = email.message_from_bytes(msg_data[0][1])
                from_header = decode_mime_words(msg.get('From', ''))
                subject = decode_mime_words(msg.get('Subject', ''))
                date = msg.get('Date', '')[:24]
                
                print(f"📧 From: {from_header}")
                print(f"   Subject: {subject}")
                print(f"   Date: {date}")
                print(f"   ID: {msg_id.decode()}")
                print("-" * 50)
        
        mail.close()
        mail.logout()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def list_attachments(args, config):
    """列出附件"""
    try:
        mail = imaplib.IMAP4_SSL(config['imap_server'], config['imap_port'])
        mail.login(config['email'], config['password'])
        
        # 发送 IMAP ID
        imap_id = config['imap_id']
        id_str = f'("name" "{imap_id["name"]}" "version" "{imap_id["version"]}" "vendor" "{imap_id["vendor"]}" "support-email" "{imap_id["support_email"]}")'
        mail.xatom('ID', id_str)
        
        # 选择文件夹
        folder = args.folder or config['defaults']['folder']
        mail.select(folder)
        
        # 获取邮件
        msg_id = str(args.id).encode()
        status, msg_data = mail.fetch(msg_id, '(RFC822)')
        if status != 'OK':
            print(f"❌ 无法获取邮件：{args.id}")
            return
        
        msg = email.message_from_bytes(msg_data[0][1])
        
        # 查找附件
        attachments = []
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            
            filename = part.get_filename()
            if filename:
                filename = decode_mime_words(filename)
                attachments.append({
                    'filename': filename,
                    'payload': part.get_payload(decode=True)
                })
        
        if attachments:
            print(f"📎 Attachments for message {args.id}:\n")
            for i, att in enumerate(attachments, 1):
                size = len(att['payload'])
                print(f"   {i}. {att['filename']} ({size:,} bytes)")
            
            # 下载附件
            if args.download:
                output_dir = os.path.expanduser(args.output or config['defaults']['output_dir'])
                os.makedirs(output_dir, exist_ok=True)
                
                print(f"\n💾 Downloading to: {output_dir}")
                for att in attachments:
                    filepath = os.path.join(output_dir, att['filename'])
                    with open(filepath, 'wb') as f:
                        f.write(att['payload'])
                    print(f"   ✅ {att['filename']}")
        else:
            print("   (没有附件)")
        
        mail.close()
        mail.logout()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='📧 email-163-com - 163 邮箱邮件管理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  email-163-com init                          # 初始化配置
  email-163-com send --to x@example.com --subject "Hi" --body "Hello!"
  email-163-com read --count 10
  email-163-com folders
  email-163-com search --from "Cloudflare"
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # init 命令
    subparsers.add_parser('init', help='初始化配置')
    
    # send 命令
    send_parser = subparsers.add_parser('send', help='发送邮件')
    send_parser.add_argument('--to', required=True, help='收件人')
    send_parser.add_argument('--subject', required=True, help='主题')
    send_parser.add_argument('--body', help='正文内容')
    send_parser.add_argument('--html', help='HTML 正文')
    send_parser.add_argument('--file', help='从文件读取正文')
    send_parser.add_argument('--attach', action='append', help='附件文件（可多次）')
    
    # read 命令
    read_parser = subparsers.add_parser('read', help='读取邮件')
    read_parser.add_argument('--folder', help='文件夹名')
    read_parser.add_argument('--count', type=int, help='邮件数量')
    read_parser.add_argument('--unread', action='store_true', help='只显示未读')
    read_parser.add_argument('--full', action='store_true', help='读取完整邮件')
    read_parser.add_argument('--id', type=int, help='邮件 ID')
    
    # folders 命令
    subparsers.add_parser('folders', help='列出文件夹')
    
    # search 命令
    search_parser = subparsers.add_parser('search', help='搜索邮件')
    search_parser.add_argument('--from', dest='from_addr', help='发件人')
    search_parser.add_argument('--subject', help='主题')
    search_parser.add_argument('--to', help='收件人')
    search_parser.add_argument('--folder', help='文件夹')
    search_parser.add_argument('--count', type=int, help='结果数量')
    
    # attachments 命令
    attach_parser = subparsers.add_parser('attachments', help='管理附件')
    attach_parser.add_argument('--id', type=int, required=True, help='邮件 ID')
    attach_parser.add_argument('--folder', help='文件夹')
    attach_parser.add_argument('--download', action='store_true', help='下载附件')
    attach_parser.add_argument('--output', help='输出目录')
    
    args = parser.parse_args()
    
    # 加载配置
    config = load_config()
    
    # 执行命令
    if args.command == 'init':
        init_config()
    elif args.command == 'send':
        send_email(args, config)
    elif args.command == 'read':
        read_emails(args, config)
    elif args.command == 'folders':
        list_folders(args, config)
    elif args.command == 'search':
        search_emails(args, config)
    elif args.command == 'attachments':
        list_attachments(args, config)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
