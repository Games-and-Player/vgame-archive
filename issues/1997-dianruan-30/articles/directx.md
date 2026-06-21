---
issue: 1997-dianruan-30
title: "DirectX与Direct3D"
section: "PC CHANNEL"
pdf_pages: [76, 77]
mag_pages: [58, 59]
author: "卓灵"
games: []
status: done
---

# DirectX 与 Direct3D

## Microsoft 进军游戏界的利器

文／卓灵

那天笔者跟好友小 Z 聊天，谈到 PC 游戏自然会眉飞色舞。大家都喜欢在网络上玩 DOOM，DUKE3D，QUAKE，然而笔者更想知道这样出色的游戏究竟如何造成。

小 Z 曾经有设计程序的经验，虽不是专业编写游戏，但加上平日多看电脑书籍杂志，对于 PC 游戏自有一番见解。

小 Z 说：“写一个 PC 游戏，尤其是动作、射击游戏，最重视的是显示速度，而以现在 PC 系统的结构，其实有许多因素不利于撰写 PC 游戏，如 DOS 真实模式下的区段定址法（Segment/Offset Addressing），做成 640KB 内存的限制，和配置最大内存空间只有 64KB 的不便，又如标准的 VGA 显示模式，通常用到的只有 320X200X256 色（Int 13h），若用取巧的方法改动 VGA 的 Register 数值也可做到 320X400 的解析度。我们现在的 SVGA 显示卡解析度往往可达 800X600，甚至可能更高。要用尽 SVGE 的能力，程序师必需要直接控制 SVGA 卡，可惜各家 SVGA 品牌太多，标准混乱，难成气候。后来业界有所谓的 VESA 显示模式的 SVGA 标准，但到近年间才见有游戏支持，但是因为解析度太高需要搬移大量资料，往往影响速度。”

笔者说：“原来编写一个游戏，程序师要面对这样多的难题。如果在 Windows 的环境，游戏设计不必受 DOS 的限制，而解析度也可以轻易提高。但是出色的 Windows 游戏真是凤毛麟角，而 PC 游戏仍是以 DOS 为主流！”

小 Z 说：“Windows 似乎是很好的写游戏平台，但是因为 Windows 有其自己的规矩，显示系统结构不容许程序师直接控制硬件，兼容问题不用顾虑之余，缺点是显示速度自然大打折扣。另外，Windows 3.1 内存管理不完善，虽说是在保护模式运行，但仍不能完全摆脱 DOS 的区段定址法，程序设计往往有所限制。到了 Windows 95，号称 32-BIT 作业系统，除了多线作业（Multithreading）外，最吸引 DOS 程序师的地方是那保护模式下的线性定址法（Flat Addressing），内存空间的运用就能得心应手了。另一方面，PC 游戏始终是占用大量系统资源的程序，为了追求更高速度和变化多端的画面技巧，程序师往往喜欢直接操控硬件。作业系统掌握所有硬件资源，对于程序师来说这个严厉的管家规矩太多了，反而有碍游戏软件的创作。”

笔者说：“那也不见得，许多在 DOS 运行得很好的游戏在 Windows 95 的 DOS Session 都没有问题。当然，有更多 DOS 游戏需要特别处理，而有部分游戏根本不能兼容 Windows 95。究其原因，就是 Windows 95 不能忍受那些垄断系统控制权的程序。近年来，Windows 游戏异军突起，俨然有成为一股潮流之势。虽然多数是加入许多电影片段的多媒体游戏（如《幽魂》），但是讲求速度的射击游戏，也会在 Windows 的平台上出现。”

小 Z 说：“在 Windows 95 推出之前，微软已想使 Windows 95 成为一个为个人用户而设计的作业系统，故此在用户界面（GUI）和即插即用所下的功夫，远比系统设计的改良要多。微软自然不会放过 PC 游戏这个庞大的市场。微软不擅于发行游戏，它的强项是作业系统。它当然希望所有人都会用它出品的作业系统玩所有 PC 游戏。”

笔者说：“最好是 PC 游戏都为 Windows 95 而写，但 Windows 95 又不是理想的游戏平台，那么，微软有什么办法吸引程序师为 Windows 95 写游戏呢？”

小 Z 说：“微软最喜欢建立标准，在游戏方面，它为 Windows 95/NT 平台，提供一个专为 PC 游戏设计的 API 标准——DirectX，说不定会给未来 Windows 游戏带来新的冲激。”

笔者说：“什么是 DirectX？有什么好处？”

小 Z 说：“DirectX 是由一系列硬件驱动（如显示卡，音效卡等）组成，其主要的元件有 DirectDraw，DirectInput，DirectPlay，和 DirectSound，分别针对显示、Joystick 控制、网络通讯和音效等各方面。DirectX 最大的好处是提供有效率的驱动而使游戏设计的程序界面（API）得以统一，使程序可以做到 Hardware Independency。”

笔者说：“Hardware Independency 在 Windows 3.1 时已有提倡。那不单可以增加程序本身的可携性（Portability），亦可使程序师不必花时间去学习控制复杂难懂的硬件。程序师只需懂得一种 API，不必为支持不同形式的显示模式和不同种类的显示卡而大伤脑筋。”

小 Z 说：“是的，编写游戏的复杂程序远超一般人想像。如果对硬件一无所知，程序设计经验的底子不厚，根本不能成就。有了 DirectX，便可减少设计 PC 游戏的难度，而程序师便可以集中处理游戏设计的工作，例如内容和可玩性。此外，DirectX 专门处理显示的单元（DirectDraw），它的驱动提供的不单是高解析度且色彩更加丰富的显示模式，最重要的是它能使程序能以下利用 Windows 显示加速卡的特点。”

笔者说：“你说 DirectX 能善用 Windows 显示加速卡，据我所知，许多 Windows 显示加速卡的标准的 VGA 模式下只是透过 BIOS 画点，或者直接改显示内存的内容，表现与普通的 VGA 卡相差无几。到了 Windows 环境，透过 Windows 的 GDI（Graphic Device Interface）来画线、圆及几何图形，才可以显示加速卡的威力。DirectX 真的可以让游戏利用硬件加速吗？”

小 Z 说：“微软是这样说的。但是对于 2D 画面如制作动画效果，让许多张 Bitmap 在画面显示，其实是相当于把大量资料在主内存与显示内存之间搬移。DirectX 中处理显示的元件 DirectDraw 本质上是显示内存的管理员。在它的统辖下，程序可以直接存取显示内存，也可以作显示页的快速切换，这些功能是 Windows 本身不能提供的。至于显示加速卡能大派用场的地方，应该是 3D 画面的处理。如 Alone In the Dark，Doom，Quake 等游戏应用了 3D 画面的技巧，虽然方法有所出入，但是一样要涉及点、线、面的几何图形的计算和显示；某些情况要处理大量浮点运算（Floating Point Math.），尤其是全彩高解析的 Ray Tracing 画面（例如 3D STUDIO）。如果这些计算交由硬件处理，肯定会提高游戏的效率。”

笔者说：“DirectX 也有提供 3D 画面的处理吗？”

小 Z 说：“DirectX 不包括 3D 画面的处理，而是交由 Direct3D 去做。”

笔者说：“真正用到 Windows 显示加速卡功能的是 Direct3D！那么 Direct3D 怎样物尽其用？”

小 Z 说：“Direct3D 提供两种模式——Retained mode 和 immediate mode。前者定义好一个 3D Engine，程序师只要输入 3D 物件的信息（如坐标、结构）和预定的贴图，使用几个简单指令便可以使 3D 物件转动和改变比例。后者是比较低层次的硬件呼叫，提供一个渠道让程序师能使用硬件的显示加速功能。”

笔者说：“DirectX 和 Direct3D 看来相当不错，我们从那里可以得到？是否需要特别的准备？”

小 Z 说：“DirectX 和 Direct3D 都是为程序开发而设计的。玩家不需要特别安装软件，因为当你玩到一些用 DirectX 和 Direct3D 设计的游戏，游戏安装程序自然将需要的元件（Run time Components）安装到你的 PC 上。据我所知，EarthSeige II 的 Windows 95 版、The Rise and Rule Of Ancient Empire 和 chaos Overlords for Windows 95 都已采用 DirectX（软体动物按：实际上目前已经有许多的游戏用上了 DirectX）。各大显示卡制造商如 Cirrus Logic，S3，Trident，Tseng lab，都有参与支持 Direct3D，软件开发商如 Acclaim，Activision，id Software，Infogrames 都开始为 Direct3D 设计游戏。如果你对游戏程序有兴趣，可以到微软的 homepage 的 software library 下传最新的 Direct SDK（Software Development Kit）回来研究一下。”

笔者说：“如果 DirectX 和 Direct3D 真的得到业界支持，诚然是美事。然而微软的'统一大业'形势也不是人人赞同的。如果 DirectX 和 Direct3D 做不出一个象样的游戏，我们仍有一段日子要玩 DOS 游戏呢。”

本文摘自香港《电脑时代》杂志

## 编辑备注

- 原文跨 PDF p.76–77（刊页 58–59）。
- 文章以对话体写成，笔者与“小 Z”（有设计程序经验的好友）问答形式介绍 DirectX 及 Direct3D。
- 文末注明“本文摘自香港《电脑时代》杂志”，p.77 同时附有《电子游戏软件》杂志订阅办法的广告（邮发代号 82-648，每期 6.40 元），未纳入正文。
- “DirectX 最大的好处是……Hardware Independency”：原文使用英文术语，照原文转录。
- “chaos Overlords”原文小写 c，照录。
- PDF p.75 为广告页（天津任天龙、上海 GAME 霸王馆、北京腾达游戏、湖南郴州奋斗乐商行），不属于本文。
