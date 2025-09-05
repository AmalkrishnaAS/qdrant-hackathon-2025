
  import React from "react";
  
  import { Button } from "@/components/ui/button";
  import { Separator } from "@/components/ui/separator";
import { IconPlayerPlay, IconPlayerPlayFilled } from "@tabler/icons-react";
  
  interface ListItem {
    icon: React.ReactNode;
    title: string;
    category: string;
    description: string;
    link: string;
  }
  
  interface List2Props {
    heading?: string;
    items?: ListItem[];
  }
  
  const List2 = ({
    heading,
    items=[],
  }: List2Props) => {
    return (
      <section className="py-4">
        <div className="container px-0">
          <h1 className="mb-6 px-4 text-2xl font-semibold md:text-3xl">
            {heading}
          </h1>
          <div className="flex flex-col ">
            <Separator />
            {items.map((item, index) => (
              <React.Fragment key={index}>
                <div className="grid items-center gap-3 px-3 py-3 md:grid-cols-2 hover:bg-muted/50 transition-colors rounded-lg grid-cols-2">
                  <div className="order-2  flex items-center gap-2 md:order-none">
                    <span className="flex mr-4  h-12 w-12 shrink-0 items-center justify-center rounded-md bg-muted">
                      {item.icon}
                    </span>
                    <div className="flex flex-col gap-1">
                      <h3 className="font-semibold">{item.title}</h3>
                      <p className="text-sm text-muted-foreground">
                        {item.category}
                      </p>
                    </div>
                  </div>
                  {/* <p className="order-1 text-lg font-medium md:order-none md:col-span-2 line-clamp-1">
                    {item.description}
                  </p> */}
                  <Button variant="ghost" size="sm" asChild className="order-3 ml-auto w-fit h-8 px-3">
                <IconPlayerPlay />
                   </Button>
                </div>
                <Separator />
              </React.Fragment>
            ))}
          </div>
        </div>
      </section>
    );
  };
  
  export { List2 };
  