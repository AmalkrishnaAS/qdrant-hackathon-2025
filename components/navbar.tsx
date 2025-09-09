import React from "react";
import { FloatingDock } from "@/components/ui/floating-dock";
import {
  IconBrandGithub,
  IconBrandX,
  IconClock,
  IconCompass,
  IconExchange,
  IconHome,
  IconMusic,
  IconNewSection,
  IconSettings,
  IconSettings2,
  IconSparkles,
  IconTerminal2,
  IconTrendingUp,
} from "@tabler/icons-react";

export function FloatingDockDemo() {
  const links = [
    {
      title: "Create",
      icon: (
        <IconSparkles className="h-full w-full text-neutral-500 dark:text-neutral-300" />
      ),
      href: "/",
    },

    {
      title: "Library",
      icon: (
        <IconMusic className="h-full w-full text-neutral-500 dark:text-neutral-300" />
      ),
      href: "/library",
    },
    {
      title: "Explore",
      icon: (
        <IconCompass className="h-full w-full text-neutral-500 dark:text-neutral-300" />
      ),
      href: "explore",
    },
    {
      title: "Trending Music",
      icon: (
        <IconTrendingUp className="h-full w-full text-neutral-500 dark:text-neutral-300" />

      ),
      href: "trending",
    },
    {
      title: "Settings",
      icon: (
        <IconSettings className="h-full w-full text-neutral-500 dark:text-neutral-300" />
      ),
      href: "/settings",
    },

    {
      title: "Tasks",
      icon: (
        <IconClock className="h-full w-full text-neutral-500 dark:text-neutral-300" />
      ),
      href: "tasks",
    },
    {
      title: "Contribute",
      icon: (
        <IconBrandGithub className="h-full w-full text-neutral-500 dark:text-neutral-300" />
      ),
      href: "#",
    },
  ];
  return (
    <div className="w-full flex justify-center">
      <FloatingDock
        items={links}
        desktopClassName="bg-white/10 backdrop-blur-lg rounded-full p-2 border border-gray-200/20 shadow-lg"
        mobileClassName="bg-white/10 backdrop-blur-lg rounded-full p-2 border border-gray-200/20 shadow-lg"
      />
    </div>
  );
}
